from dataclasses import dataclass
from enum import IntEnum

from backend.isa import ALUOp, MemOp, BranchOp, CallRetOp, DecOp, Register

@dataclass
class ISAInstruction:
    op: IntEnum
    rs1: Register = Register.R0
    rs2: Register = Register.R0
    rd: Register = Register.R0
    imm: int = 0
    dec_op: DecOp = DecOp.CALC_REG

@dataclass
class ISACalcReg(ISAInstruction):
    dec_op: DecOp = DecOp.CALC_REG

@dataclass
class ISACalcImm(ISAInstruction):
    dec_op: DecOp = DecOp.CALC_IMM

@dataclass
class ISAMemLoad(ISAInstruction):
    dec_op: DecOp = DecOp.MEM_LOAD

@dataclass
class ISAMemStore(ISAInstruction):
    dec_op: DecOp = DecOp.MEM_STOR

@dataclass
class ISACallRet(ISAInstruction):
    dec_op: DecOp = DecOp.CALL_RET

@dataclass
class ISABranch(ISAInstruction):
    dec_op: DecOp = DecOp.BRANCH