from __future__ import annotations

from dataclasses import dataclass
from typing import List
from .values import *


@dataclass
class IRInstruction:
    pass

    def used_temps(self) -> List[IRTemp]:
        return []

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

    def used_temps(self) -> List[IRTemp]:
        used = []
        if isinstance(self.src, IRTemp):
            used.append(self.src)
        return used


@dataclass
class BinOpIRInstruction(IRInstruction):
    left: IRTemp
    right: IRTemp | IRConst
    op: str
    dst: IRTemp

    def __repr__(self):
        return f"BinOpIRInstruction(left={self.left}, right={self.right}, op='{self.op}', dst={self.dst})"

    def used_temps(self) -> List[IRTemp]:
        used = []
        if isinstance(self.left, IRTemp):
            used.append(self.left)
        if isinstance(self.right, IRTemp):
            used.append(self.right)
        return used

@dataclass
class PrintIRInstruction(IRInstruction) :
    value: IRValue

    def __repr__(self):
        return f"PrintIRInstruction(value={self.value})"

    def used_temps(self) -> List[IRTemp]:
        used = []
        if isinstance(self.value, IRTemp):
            used.append(self.value)
        return used
    
__all__ = ['IRInstruction', 'ConstIRInstruction', 'LoadIRInstruction',
           'StoreIRInstruction', 'BinOpIRInstruction', 'PrintIRInstruction']
