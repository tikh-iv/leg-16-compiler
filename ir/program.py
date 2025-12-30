from dataclasses import dataclass
from typing import List
from .instructions import *
from .values import *


@dataclass
class ProgrammIRInstruction:
    instructions: List[IRInstruction]
    slots: List[IRSlot]

    def __repr__(self):
        return f"ProgramIRInstruction(instructions={self.instructions}, slots={self.slots})"
    
__all__ = ['ProgrammIRInstruction']