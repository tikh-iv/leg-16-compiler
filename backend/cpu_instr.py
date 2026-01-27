from dataclasses import dataclass

from backend.isa import ALUOp, MemOp, BranchOp, CallRetOp, DecOp, Register

@dataclass
class CalcReg:
    op: ALUOp
    rs1: Register
    rs2: Register
    rd: Register
    dec_op: DecOp = DecOp.CALC_REG

@dataclass
class CalcImm:
    op: ALUOp
    rs1: Register
    imm: int
    rd: Register
    dec_op: DecOp = DecOp.CALC_IMM

@dataclass
class MemLoad:
    op: MemOp
    rd: Register
    address: int
    dec_op: DecOp = DecOp.MEM_LOAD

@dataclass
class MemStore:
    op: MemOp
    rs1: Register
    address: int
    dec_op: DecOp = DecOp.MEM_STOR

@dataclass
class CallRet:
    op: CallRetOp
    address: int
    dec_op: DecOp = DecOp.CALL_RET

@dataclass
class Branch:
    op: BranchOp
    address: int
    dec_op: DecOp = DecOp.BRANCH