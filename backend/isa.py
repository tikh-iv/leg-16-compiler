from enum import IntEnum


class Register(IntEnum):
    R0  = 0b000
    R1  = 0b001
    R2  = 0b010
    R3  = 0b011
    R4  = 0b100
    R5  = 0b101
    MAR = 0b110
    IO  = 0b111


class DecOp(IntEnum):
    CALC_REG = 0b000
    CALC_IMM = 0b001
    MEM_LOAD = 0b010
    _NONE_3  = 0b011
    CALL_RET = 0b100
    BRANCH   = 0b101
    _NONE_6  = 0b110
    MEM_STOR = 0b111


class ALUOp(IntEnum):
    ADD  = 0b0000
    SUB  = 0b0001
    AND  = 0b0010
    OR   = 0b0011
    NOT  = 0b0100
    XOR  = 0b0101
    SHL  = 0b0110
    SHR  = 0b0111
    MUL  = 0b1000
    MULH = 0b1001
    DIV  = 0b1010
    DIVH = 0b1011
    _NONE_11 = 0b1100
    MOV  = 0b1101
    ROL  = 0b1110
    ROR  = 0b1111

class BranchOp(IntEnum):
    BLE  = 0b0000
    BLT  = 0b0001
    BGE  = 0b0010
    BGT  = 0b0011
    BLEU = 0b0100
    BLTU = 0b0101
    BGEU = 0b0110
    BGTU = 0b0111
    BEQ  = 0b1000
    BNE  = 0b1001
    _NONE_10 = 0b1010
    _NONE_11 = 0b1011
    _NONE_12 = 0b1100
    _NONE_13 = 0b1101
    _NONE_14 = 0b1110
    JUMP = 0b1111

class MemOp(IntEnum):
    PUSH = 0b0000
    POP  = 0b0001
    STOR = 0b0010
    LOAD = 0b0011