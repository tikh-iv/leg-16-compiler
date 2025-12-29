from dataclasses import dataclass
from typing import List
from .values import *


@dataclass
class IRInstruction:
    pass

@dataclass
class ConstIRInstruction(IRInstruction):
    src: IRConst
    dst: IRTemp

@dataclass 
class LoadIRInstruction(IRInstruction):
    src: IRSlot
    dst: IRTemp

@dataclass
class StoreIRInstruction(IRInstruction):
    src: IRValue
    dst: IRSlot

@dataclass
class BinOpIRInstruction(IRInstruction):
    left: IRValue
    right: IRValue
    op: str
    dst: IRTemp

@dataclass
class PrintIRInstruction(IRInstruction) :
    value: IRValue

