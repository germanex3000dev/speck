#!/usr/bin/env python3
"""Drive ./null through a pty and check that the file ends up correct."""
import os, pty, select, sys, time, tempfile

PROG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "null")

def run(initial, keys, name="t.txt"):
    d = tempfile.mkdtemp()
    path = os.path.join(d, name)
    if initial is not None:
        with open(path, "w") as f:
            f.write(initial)
    pid, fd = pty.fork()
    if pid == 0:
        os.execv(PROG, [PROG, path])
    time.sleep(0.25)
    out = b""
    def drain(t=0.08):
        nonlocal out
        end = time.time() + t
        while time.time() < end:
            r, _, _ = select.select([fd], [], [], 0.02)
            if r:
                try:
                    chunk = os.read(fd, 65536)
                except OSError:
                    return
                if not chunk:
                    return
                out += chunk
    drain()
    for k in keys:
        os.write(fd, k)
        drain()
    os.write(fd, b"\x11")          # Ctrl-Q (saves)
    drain(0.2)
    _, status = os.waitpid(pid, 0)
    with open(path, "rb") as f:
        return f.read(), out, status

cases = []

def case(desc, initial, keys, expected):
    cases.append((desc, initial, keys, expected))

case("insert at start", "hello\n", [b"X"], b"Xhello\n")
case("insert newline", "", [b"a", b"\r", b"b"], b"a\nb")
case("backspace at end", "abc", [b"\x1b[F", b"\x7f", b"\x7f"], b"a")
case("backspace at start", "abc", [b"\x7f"], b"abc")
case("append at end", "ab", [b"\x1b[F", b"c"], b"abc")
case("down keeps column", "abcdef\nxy\n", [b"\x1b[F", b"\x1b[B", b"Z"], b"abcdef\nxyZ\n")
case("up then type", "abc\ndef\n", [b"\x1b[B", b"\x1b[A", b"X"], b"Xabc\ndef\n")
case("home/end", "line\n", [b"\x1b[F", b"\x1b[H", b"^"], b"^line\n")
case("insert in middle", "ac", [b"\x1b[C", b"b"], b"abc")
case("scroll to bottom", "".join(f"l{i}\n" for i in range(60)),
     [b"\x1b[B"] * 59 + [b"Z"], ("".join(f"l{i}\n" for i in range(59)) + "Zl59\n").encode())
case("delete empty is safe", "", [b"\x7f", b"\x1b[A", b"\x1b[B", b"\x1b[D", b"\x1b[C"], b"")
case("wide line + burst", "", [b"x" * 200], b"x" * 200)
case("burst with newlines", "", [b"ab\ncd\nef"], b"ab\ncd\nef")
case("arrow burst", "".join(f"line {i}\n" for i in range(60)),
     [b"\x1b[B" * 40, b"Z"],
     ("".join(f"line {i}\n" for i in range(40)) + "Zline 40\n"
      + "".join(f"line {i}\n" for i in range(41, 60))).encode())

fails = 0
for desc, initial, keys, expected in cases:
    got, out, status = run(initial, keys)
    ok = got == expected if expected is not None else got.endswith(b"Z\n")
    if not ok:
        fails += 1
    print(("PASS " if ok else "FAIL ") + desc + f"  -> {got[:60]!r}")

print("\nall good" if fails == 0 else f"\n{fails} failure(s)")
sys.exit(1 if fails else 0)
