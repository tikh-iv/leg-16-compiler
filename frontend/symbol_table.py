from dataclasses import dataclass
import logging
from frontend.ast_leg import VarDecl, BinaryOp, Number, VarRef, Program, Print, Node, IfStmt, Block, WhileStmt

logger = logging.getLogger('semantic')

@dataclass
class Symbol:
    name: str
    slot: int

class SymbolTable:
    def __init__(self):
        self.symbols: dict[str, Symbol] = {}
        self.next_slot = 0

    def declare(self, name) -> Symbol:
        sym = Symbol(name=name, slot=self.next_slot)
        if name in self.symbols:
            logger.debug(f"{name} already declared {self.symbols}")
        else:
            self.symbols[name] = sym
            self.next_slot += 1
        return sym

    def lookup(self, name) -> Symbol:
        if name not in self.symbols:
            raise Exception(f"{name} not declared in {self.symbols}")
        return self.symbols[name]
    
    def all_slots(self) -> list[int]:
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
            self.table.declare(node.name)
            logger.debug(f"{node.name} declared")
            self.visit(node.expr)

        elif isinstance(node, BinaryOp):
            self.visit(node.left)
            self.visit(node.right)

        elif isinstance(node, VarRef):
            self.table.lookup(node.name)

        elif isinstance(node, IfStmt):
            self.visit(node.condition)
            self.visit(node.then_block)
            self.visit(node.else_block)

        elif isinstance(node, WhileStmt):
            self.visit(node.condition)
            self.visit(node.body_block)

        elif isinstance(node, Block):
            for block_node in node.statements:
                self.visit(block_node)

        elif isinstance(node, Number):
            pass

        elif isinstance(node, Print):
            self.visit(node.expr)
