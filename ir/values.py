from dataclasses import dataclass


@dataclass
class IRValue:
    pass


@dataclass
class IRTemp(IRValue):
    id: int

    def __repr__(self):
        return f"IRTemp({self.id})"
 

@dataclass
class IRConst(IRValue):
    value: int

    def __repr__(self):
        return f"IRConst({self.value})"


@dataclass
class IRSlot(IRValue):
    index: int
    name: str
    def __repr__(self):
        return f"IRSlot(index={self.index}, name='{self.name}')"


@dataclass
class IRLabel(IRValue):
    index: int
    def __repr__(self):
        return f"IRLabel(index={self.index})"


__all__ = ['IRValue', 'IRTemp', 'IRConst', 'IRSlot']