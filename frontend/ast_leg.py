from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


class Node: pass

class Expr(Node): pass

class Stmt(Node): pass

@dataclass
class Block(Stmt):
    statements: List[Stmt]

@dataclass
class Number(Expr):
    value: int

    def __repr__(self) -> str:
        return f"Number({self.value})"

@dataclass
class VarRef(Expr):
    name: str

    def __repr__(self) -> str:
        return f"VarRef({self.name})"

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
class IfStmt(Stmt):
    condition: BinaryOp
    then_block: Block
    else_block: Block | None

    def __repr__(self):
        return f"IfStmt(Condition: {self.condition}. Then: {self.then_block}. Else: {self.else_block}.)"

@dataclass
class Program(Node):
    statements: List[Stmt]

    def __repr__(self):
        return f"Program({self.statements})"
