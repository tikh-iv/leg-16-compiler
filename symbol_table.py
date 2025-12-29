from dataclasses import dataclass
import logging
from ast_leg import VarDecl, BinaryOp, Number, VarRef, Program, Print, Stmt, Expr, Node
from ir.instructions import IRSlot

logger = logging.getLogger('semantic')

@dataclass
class Symbol:
    name: str
    slot: IRSlot

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.next_slot = 0

    def declare(self, name) -> Symbol:
        if name in self.symbols:
            raise Exception(f"{name} already declared")
        slot = IRSlot(index=self.next_slot, name=name)
        sym = Symbol(name=name, slot=slot)
        self.symbols[name] = sym
        self.next_slot += 1
        return sym

    def lookup(self, name) -> str:
        if name not in self.symbols:
            raise Exception(f"{name} not declared")
        return self.symbols[name]
    
    def all_slots(self) -> list[IRSlot]:
        return [sym.slot for sym in self.symbols.values()]



class SemanticAnalyzer:
    def __init__(self):
        self.table = SymbolTable()

    def visit(self, node: Node) -> None:
        logger.debug(f"Visiting {type(node).__name__}")

        if isinstance(node, Program):
            for s in node.statements:
                self.visit(s)

        elif isinstance(node, VarDecl):
            sym = self.table.declare(node.name)
            self.visit(node.expr)

        elif isinstance(node, BinaryOp):
            self.visit(node.left)
            self.visit(node.right)

        elif isinstance(node, VarRef):
            self.table.lookup(node.name)

        elif isinstance(node, Number):
            pass

        elif isinstance(node, Print):
            self.visit(node.expr)
