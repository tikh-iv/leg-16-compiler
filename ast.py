from typing import List


class Node: pass

class Expr(Node): pass

class Stmt(Node): pass

class Number(Expr):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def __repr__(self) -> str:
        return f"Number({self.value})"

class VarRef(Expr):
    def __init__(self, name: str) -> None:
        self.name: str = name

    def __repr__(self) -> str:
        return f"Name({self.name})"

class BinaryOp(Expr):
    def __init__(
            self,
            left: Expr,
            op: str,
            right: Expr
    ) -> None:
        self.left: Expr = left
        self.op: str = op
        self.right: Expr = right

    def __repr__(self) -> str:
        return f"BinaryOp({self.left}, {self.op}, {self.right})"

class VarDecl(Stmt):
    def __init__(
            self,
            name: str,
            expr: Expr
    ) -> None:
        self.name: str = name
        self.expr: Expr = expr

    def __repr__(self) -> str:
        return f"VarDecl({self.name}, {self.expr})"

class Print(Stmt):
    def __init__(self, expr: Expr) -> None:
        self.expr: Expr = expr

    def __repr__(self):
        return f"Print({self.expr})"


class Program(Node):
    def __init__(self, statements: List[Stmt]) -> None:
        self.statements: List[Stmt] = statements

    def __repr__(self):
        return f"Program({self.statements})"
