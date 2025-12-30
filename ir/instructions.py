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

    def __repr__(self):
        return f"ConstIRInstruction(src={self.src}, dst={self.dst})"    
    

@dataclass 
class LoadIRInstruction(IRInstruction):
    src: IRSlot
    dst: IRTemp

    def __repr__(self):    
        return f"LoadIRInstruction(src={self.src}, dst={self.dst})"
    

@dataclass
class StoreIRInstruction(IRInstruction):
    src: IRValue
    dst: IRSlot

    def __repr__(self):
        return f"StoreIRInstruction(src={self.src}, dst={self.dst})"


@dataclass
class BinOpIRInstruction(IRInstruction):
    left: IRValue
    right: IRValue
    op: str
    dst: IRTemp

    def __repr__(self):
        return f"BinOpIRInstruction(left={self.left}, right={self.right}, op='{self.op}', dst={self.dst})"
    

@dataclass
class PrintIRInstruction(IRInstruction) :
    value: IRValue

    def __repr__(self):
        return f"PrintIRInstruction(value={self.value})"
    
__all__ = ['IRInstruction', 'ConstIRInstruction', 'LoadIRInstruction',
           'StoreIRInstruction', 'BinOpIRInstruction', 'PrintIRInstruction']
