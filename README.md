This program compiles RISC-V assembly code into Circuitverse EEPROM JSONs.
It does not support all operations, but it does support:
add, sub, and, or, xor, addi, andi, ori, xori, lw, sw
With planned support for:
beq, bne, bge, blt*

How to use it:
This program reads from standard in. To compile the file myprogram.s, you can do $python compiler.py < myprogram.s
The JSON will be printed on standard out. 
I have commented out code that will also copy the JSON to the clipboard for easy pasting into Circuitverse. I didn't want anybody to unintentionally lose data on their clipboard, or to need to install pyperclip. If this feature is appealing you can go in and re-enable it.
Currently, only the lower 16 registers are supported, and only with their standard names (a0, t0, etc.)


*I have been told that we invented another format for these instructions that was easier to build a circuit for. Until I find out what this format is, B-type instructions will be unsupported. I could implement the 'real' format, but this wouldn't be that useful.

