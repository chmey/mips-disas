#!/usr/bin/python3

import struct

reg_ip = 0x0
entry_addr = 0x0

registers = {
    0: "zero",
    1: "at",
    2: "v0",
    3: "v1",
    4: "a0",
    5: "a1",
    6: "a2",
    7: "a3",
    8: "t0",
    9: "t1",
    10: "t2",
    11: "t3",
    12: "t4",
    13: "t5",
    14: "t6",
    15: "t7",
    16: "s0",
    17: "s1",
    18: "s2",
    19: "s3",
    20: "s4",
    21: "s5",
    22: "s6",
    23: "s7",
    24: "t8",
    25: "t9",
    26: "k0",
    27: "k1",
    28: "gp",
    29: "sp",
    30: "fp",
    31: "ra",
}


def dis_not_implemented(instruction_bytes):
    global reg_ip
    opcode = get_opcode(instruction_bytes)
    print("Error! Not implemented opcode ({:x}) at IP 0x{:x}".format(opcode, reg_ip))
    exit(1)


def disassemble_R_type(instruction_bytes):
    global reg_ip
    """
    Disassemble and print a MIPS R type instruction.
    """
    if instruction_bytes == 0:
        print("nop")
        return
    function_code = get_function_code(instruction_bytes)
    rd = (instruction_bytes & 0x000F800) >> 11
    rt = (instruction_bytes & 0x01F0000) >> 16
    if (function_code < 0x04):
        # Shifting, utilize shamt
        shamt = (instruction_bytes & 0x000007C0) >> 6
        print(f"{disas_funcodes[function_code]} ${registers[rd]},${registers[rt]}, {shamt}")
    else:
        rs = (instruction_bytes & 0x3E00000) >> 21
        print(f"{disas_funcodes[function_code]} ${registers[rd]}, ${registers[rs]}, ${registers[rt]}")


def disassemble_I_type(instruction_bytes):
    global reg_ip
    """
    Disassemble and print a MIPS I type instruction.
    """
    rs = (instruction_bytes & 0x3E00000) >> 21
    rt = (instruction_bytes & 0x01F0000) >> 16
    imm = instruction_bytes & 0x0000FFFF
    op_code = get_opcode(instruction_bytes)
    op = disas_immcodes[op_code]
    if op_code >= 0x20:
        print(f"{op} ${registers[rt]}, {imm}(${registers[rs]})")
    else:
        print(f"{op} ${registers[rt]}, ${registers[rs]}, {hex(imm)}")


def disassemble_J_type(instruction_bytes):
    global reg_ip
    """
    Disassemble and print a MIPS J type instruction.
    """
    addr = (instruction_bytes & 0x3FFFFFFF)
    op_code = get_opcode(instruction_bytes)
    print(f"{disas_jmpcodes[op_code]} {hex(addr)}")


disas_opcodes = {
    0x0: disassemble_R_type,
    0x2: disassemble_J_type,  # JUMP
    0x3: disassemble_J_type,  # JAL
    0x4: disassemble_I_type,  # BEQ
    0x8: disassemble_I_type,  # ADDI
    0x9: disassemble_I_type,  # ADDIU
    0xA: disassemble_I_type,  # SLTI
    0xB: disassemble_I_type,  # SLTIU
    0xC: disassemble_I_type,  # ANDI
    0xD: disassemble_I_type,  # ORI
    0xE: disassemble_I_type,  # XORI
    0xF: disassemble_I_type,  # LUI
    0x20: disassemble_I_type,  # LB
    0x23: disassemble_I_type,  # LW
    0x28: disassemble_I_type,  # SB
    0x2B: disassemble_I_type,  # SW
}

disas_jmpcodes = {
    0x2: "j",
    0x3: "jal",
}

disas_immcodes = {
    0x4: "beq",
    0x8: "addi",
    0x9: "addiu",
    0xA: "slti",
    0xB: "sltiu",
    0xC: "andi",
    0xD: "ori",
    0xE: "xori",
    0xF: "lui",
    0x20: "lb",
    0x23: "lw",
    0x28: "sb",
    0x2B: "sw",
}

disas_funcodes = {
    0x0: "sll",
    0x2: "srl",
    0x3: "sra",
    0x4: "sllv",
    0x6: "srlv",
    0x8: "jr",
    0xC: "syscall",
    0x10: "mfhi",
    0x12: "mflo",
    0x18: "mult",
    0x19: "multu",
    0x1A: "div",
    0x1B: "divu",
    0x20: "add",
    0x21: "addu",
    0x22: "sub",
    0x23: "subu",
    0x24: "and",
    0x25: "or",
    0x26: "xor",
    0x27: "nor",
    0x2A: "slt",
    0x2B: "sltu",
}


def get_opcode(instruction_bytes):
    """
    Returns the 6-bit MIPS opcode from a 4 byte instruction.
    """
    op = (instruction_bytes & 0xFC000000) >> (3 * 8 + 2)
    return op


def get_function_code(instruction_bytes):
    """
    Returns the 6-bit MIPS function code from a 4 byte R-type instruction.
    """
    fun = instruction_bytes & 0x3F
    return fun


def get_uint32_little_endian(some_bytes):
    return struct.unpack("<I", some_bytes)[0]


def exec_loop(data):
    global reg_ip
    while(reg_ip - entry_addr < len(data)):
        # fetch instruction
        instruction_bytes = get_uint32_little_endian(data[reg_ip - entry_addr:reg_ip + 4 - entry_addr])
        # decode opcode
        opcode = get_opcode(instruction_bytes)
        # call function code handler
        disas_opcodes.get(opcode, dis_not_implemented)(instruction_bytes)
        # increment IP
        reg_ip += 4


code = open("material/mipsel_dump.bin", 'rb').read()

exec_loop(code)
