# MIPS Disassembler & Emulator

**Beware**: The disassembler is **not** complete. It does not feature all MIPS instructions and function codes. I wrote this for passing class homework. Use at your own risk.  

As this is published under the **MIT** license, feel free to use it as you wish.  

The project consists of two parts: 

## MIPS Disassembler

There is a disassembler that parses a MIPS 32 bit binary file and prints the disassembled code.  

The disassembler opens a fixed file path and iterates over all 4 byte instructions. It will decode the instructions and print it in a human readable, disassembled format, e.g.:

```mips
ori $v0, $v0, 0xb2ae
xor $s2, $s2, $v0
nor $s2, $zero, $s2
```

## MIPS Emulator

Built on top of the disassembler, there is an emulator which starts from a fixed state and emulates the binary. In the end a certain value is computed and printed. This value was needed to pass the class homework.
