from typing import List

from ast_leg import Expr, Number, VarRef, BinaryOp, Print, VarDecl, Program
from .instructions import *
from symbol_table import Symbol, SymbolTable

import logging
logger = logging.getLogger('Builder')


class IRBuilder:
    def __init__(self, symbol_table: SymbolTable):
        self.instructions: List[IRInstruction] = []
        self.temp_counter: int = 0
        self.symbol_table: SymbolTable = symbol_table

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
            symbol: Symbol = self.symbol_table.lookup(node.name)
            temp: IRTemp = self.new_temp()
            self.emit(LoadIRInstruction(dst=temp, src=symbol.slot))
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
            symbol: Symbol = self.symbol_table.lookup(node.name)
            self.emit(StoreIRInstruction(src=expr_temp, dst=symbol.slot))
        elif isinstance(node, Print):
            expr_temp: IRTemp = self.build_expr(node.expr)
            self.emit(PrintIRInstruction(value=expr_temp))
        else:
            raise NotImplementedError(f"Statement type {type(node)} not implemented")
        
    def build_program(self, ast_tree: Program) -> PrintIRInstruction:
        logger.debug(f'Building program {ast_tree}')
        if self.instructions:
            raise Exception('IRBuilder can only build one program per instance.')
        for stmt in ast_tree.statements:
            self.build_stmt(stmt)
        return PrintIRInstruction(
            instructions=self.instructions,
            slots=self.symbol_table.all_slots()
        )