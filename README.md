# speck - The *EXTREMELY* minimalistic text-editor

`speck` is my copy of chip, another text-editor, in HEX-code. The original 
text-editor, chip was written in freestanding x86_64 Assembly. Speck doesn't
have any compilers, just the `speck.hex` executable image. 

> **Warning:** You still need a helper, this Makefile use xxd (it comes with vim),
> to convert the human readable HEX code into a binary executable.

## Build

```bash 
make
```
Yep, just make, that's all. `make` just calls the `xxd` command and makes it
executable. Simple as that, no compilers.

## Keybinds
| Keybind | Action |
| ------- | ------ |
| Ctrl+S  | Save   |
| Ctrl+Q  | Quit and Quit |
| Ctrl+C  | Save and Quit, too |

## A little info on the program
The executable binary is only 1539 bytes long (about 1.5KB), making it even 
smaller than a standard picture, or something like `echo`
RAM usage is also extremely little. Only about 12KB of RAM usage. The usage grows 
with the file size, but it's not much. A ~1800 markdown file pushed the RAM
up at 57KB, so it's alright.


