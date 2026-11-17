# null — chip as hexadecimal machine code

`null` is a byte-for-byte copy of [`chip`](../chip/), the freestanding
x86-64 Linux text editor, stored as hexadecimal instead of assembly source.
There is no `.s` file here: `null.hex` is the executable image itself.

The decoded result is identical to `chip`:

```
sha256  ef80bdcdb36a2a16af007046fc2502d485517de69e78e8a7f7271c924554fe40
size    2,408 bytes
```

## Build

```
$ make
$ ./null notes.txt
```

`make` decodes `null.hex` with `xxd -r -p` and marks the result executable.
`xxd` (part of Vim) is the only build tool needed; Python 3 is used only by
the tests.

Verify the copy and run the editor tests:

```
$ make check    # sha256sum -c null.sha256
$ make test     # pty-driven editing tests
```

Behavior is exactly that of chip: printable ASCII inserts at the cursor,
Enter inserts a newline, Backspace deletes, arrows/Home/End move, Ctrl-S
saves, and Ctrl-Q or Ctrl-C saves and quits. Without a filename it opens
`untitled.txt`.

## What is in the hex

The file is a single 2,408-byte `ET_EXEC` ELF with one read/write/execute
`PT_LOAD` segment, no section headers and no runtime dependencies. Every byte,
including the ELF headers, is present in `null.hex`.

| File offset | Size  | Contents                                      |
| ----------- | ----: | --------------------------------------------- |
| `0x000`     |    64 | ELF header                                     |
| `0x040`     |    56 | program header (`PT_LOAD`, RWE)                |
| `0x078`     | 2,177 | machine code (`.text`); entry point `0x400078` |
| `0x8f9`     |     3 | alignment padding                              |
| `0x8fc`     |   108 | read-only data: strings and divisor table      |
| —           | 65,848| `.bss` (NOBITS, occupies no file space)        |

The loadable image is mapped at `0x400078`; `.bss` extends it in memory with
the 64 KiB edit buffer and terminal state. The full layout, memory figures and
editor internals are documented in chip's README.

## Limits

Because this is a faithful copy, it inherits chip's behavior exactly: a single
64 KiB buffer (65,535 bytes of file), byte-oriented cursor movement, clipped
long lines, and no undo/search. Opening and saving a larger file truncates it.
