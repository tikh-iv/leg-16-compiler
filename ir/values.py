from dataclasses import dataclass


@dataclass
class IRValue:
    pass

@dataclass
class IRTemp(IRValue):
    id: int
 
@dataclass
class IRConst(IRValue):
    value: int

@dataclass
class IRSlot(IRValue):
    index: int
    name: str


