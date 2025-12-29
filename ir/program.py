from dataclasses import dataclass
from typing import List
from .instructions import *


@dataclass
class ProgrammIRInstruction:
    instructions: List[IRInstruction]
    slots: List[IRSlot]