from typing import List

from ast_leg import Expr, Number, VarRef, BinaryOp, Print, VarDecl, Program
from .instructions import *
from .values import *
from .program import ProgrammIRInstruction
from symbol_table import Symbol, SymbolTable

import logging
logger = logging.getLogger('Builder')


class IRBuilder:
    def __init__(self, symbol_table: SymbolTable):
        self.instructions: List[IRInstruction] = []
        self.temp_counter: int = 0
        self.symbol_table: SymbolTable = symbol_table
        self.slots_map: dict[str, IRSlot] = {}

    def get_slot(self, name: str) -> IRSlot:
        if name not in self.slots_map:
            index = self.symbol_table.lookup(name).slot
            self.slots_map[name] = IRSlot(index=index, name=name)
        return self.slots_map[name]

    def new_temp(self) -> IRTemp:
        logger.debug(f'Creating new temp: t{self.temp_counter}')
        temp = IRTemp(self.temp_counter)
        self.temp_counter += 1
        return temp
    
    def emit(self, instruction: IRInstruction) -> None:
        logger.debug(f'Emitting instruction: {instruction}')
        self.instructions.append(instruction)

    def build_expr(self, node: Expr) -> IRTemp:
        logger.debug(f'Building expression for node: {node}')
        if isinstance(node, Number):
            temp: IRTemp = self.new_temp()
            constanta: IRConst = IRConst(value=node.value)
            self.emit(ConstIRInstruction(src=constanta, dst=temp))
            return temp
        elif isinstance(node, VarRef):
            slot = self.get_slot(node.name)
            temp: IRTemp = self.new_temp()
            self.emit(LoadIRInstruction(dst=temp, src=slot))
            return temp
        elif isinstance(node, BinaryOp):
            left_temp = self.build_expr(node.left)
            right_temp = self.build_expr(node.right)
            result_temp: IRTemp = self.new_temp()
            self.emit(BinOpIRInstruction(left=left_temp, right=right_temp, op=node.op, dst=result_temp))
            return result_temp
        else:
            raise NotImplementedError(f"Expression type {type(node)} not implemented")
        
    def build_stmt(self, node) -> None:
        logger.debug(f'Building statement for node: {node}')
        if isinstance(node, VarDecl):
            expr_temp: IRTemp = self.build_expr(node.expr)
            slot = self.get_slot(node.name)
            self.emit(StoreIRInstruction(src=expr_temp, dst=slot))
        elif isinstance(node, Print):
            expr_temp: IRTemp = self.build_expr(node.expr)
            self.emit(PrintIRInstruction(value=expr_temp))
        else:
            raise NotImplementedError(f"Statement type {type(node)} not implemented")
        
    def build_program(self, ast_tree: Program) -> ProgrammIRInstruction:
        logger.debug(f'Building program {ast_tree}')
        if self.instructions:
            raise Exception('IRBuilder can only build one program per instance.')
        for stmt in ast_tree.statements:
            self.build_stmt(stmt)
        return ProgrammIRInstruction(
            instructions=self.instructions,
            slots=list(self.slots_map.values())
        )
    
__all__ = ['IRBuilder']