from typing import List, Dict

import logging

from ir import IRInstruction
from ir.instructions import LabelIRInstruction
from ir.values import IRLabel, IRValue

logger = logging.getLogger('Label Allocator')

class LabelAllocator:
    def __init__(self):
        self.labels: Dict = {}

