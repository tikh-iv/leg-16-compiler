from dataclasses import dataclass
from typing import List


class Node: pass

class Expr(Node): pass

class Stmt(Node): pass

@dataclass
class Number(Expr):
    value: int

    def __repr__(self) -> str:
        return f"Number({self.value})"

@dataclass
class VarRef(Expr):
    name: str

    def __repr__(self) -> str:
        return f"Name({self.name})"

@dataclass
class BinaryOp(Expr):
    left: Expr
    op: str
    right: Expr

    def __repr__(self) -> str:
        return f"BinaryOp({self.left}, {self.op}, {self.right})"

@dataclass
class VarDecl(Stmt):
    name: str
    expr: Expr

    def __repr__(self) -> str:
        return f"VarDecl({self.name}, {self.expr})"

@dataclass
class Print(Stmt):
    expr: Expr

    def __repr__(self):
        return f"Print({self.expr})"


@dataclass
class Program(Node):
    statements: List[Stmt]

    def __repr__(self):
        return f"Program({self.statements})"
