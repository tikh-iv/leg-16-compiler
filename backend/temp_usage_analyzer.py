from typing import Dict

from ir import ProgrammIRInstruction, IRTemp

import logging
logger = logging.getLogger('TempAnalyzer')


class TempUsageAnalyzer:
    def __init__(self,
                 program: ProgrammIRInstruction):
        self.refcount: Dict[int, int] = {}
        self.program = program

    def analyze(self) -> Dict[int, int]:
        logger.info(f'Analyzing program')
        for instruction in self.program.instructions:
            values = instruction.used_temps()
            for value in values:
                self.refcount[value.id] = self.refcount.get(value.id, 0) + 1
                logger.debug(f'Usage for temp {value.id} now is {self.refcount[value.id]}')
        return self.refcount
