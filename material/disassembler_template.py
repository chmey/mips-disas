#!/usr/bin/python2

import struct
import ctypes

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
    print("Error! Not implemented opcode ({}) at IP 0x{:x}".format(opcode, reg_ip))
    exit(1)

def disassemble_R_type(instruction_bytes):
    global reg_ip
    """
    TODO: implement here
    """
    function_code = get_function_code(instruction_bytes)
    pass

disas_opcodes = {
    0x0: disassemble_R_type
}

def get_opcode(instruction_bytes):
    """
    TODO: implement here
    """
    pass

def get_function_code(instruction_bytes):
    """
    TODO: implement here
    """
    pass

def get_uint32_little_endian(some_bytes):
    return struct.unpack("<I", some_bytes)[0]

def exec_loop(data):
    global reg_ip
    while(reg_ip-entry_addr < len(data)):
        # fetch instruction
        instruction_bytes = get_uint32_little_endian(data[reg_ip-entry_addr:reg_ip+4-entry_addr])
        # decode opcode
        opcode = get_opcode(instruction_bytes)
        # call function code handler
        disas_opcodes.get(opcode, dis_not_implemented)(instruction_bytes)
        # increment IP
        reg_ip += 4


code = open("mipsel_dump.bin").read()

exec_loop(code)
