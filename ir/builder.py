from typing import List

from frontend.ast_leg import Expr, Number, VarRef, BinaryOp, Print, VarDecl, Program, IfStmt, WhileStmt
from .instructions import *
from .instructions import BranchIRInstruction, JumpIRInstruction, LabelIRInstruction
from .values import *
from .program import ProgrammIRInstruction
from frontend.symbol_table import SymbolTable

import logging

from .values import IRLabel

logger = logging.getLogger('Builder')

def invert_op_command(op) -> str:
    op_inversion = {
        '==': '!=',
        '!=': '==',
        '>=': '<',
        '<=': '>',
        '<': '>=',
        '>': '<='
    }
    return op_inversion[op]

class IRBuilder:
    def __init__(self, symbol_table: SymbolTable):
        self.instructions: List[IRInstruction] = []
        self.temp_counter: int = 0
        self.label_counter: int = 0
        self.symbol_table: SymbolTable = symbol_table
        self.slots_map: dict[str, IRSlot] = {}

    def get_slot(self, name: str) -> IRSlot:
        if name not in self.slots_map:
            index = self.symbol_table.lookup(name).slot
            self.slots_map[name] = IRSlot(index=index, name=name)
            logger.debug(f'Slotting IRSlot {name} {index}')
        return self.slots_map[name]

    def new_temp(self) -> IRTemp:
        logger.debug(f'Creating new temp: t{self.temp_counter}')
        temp = IRTemp(self.temp_counter)
        self.temp_counter += 1
        return temp

    def new_label(self) -> IRLabel:
        logger.debug(f'Creating new label: l{self.temp_counter}')
        label = IRLabel(self.label_counter)
        self.label_counter += 1
        return label
    
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

    def build_while_stmt(self, node:WhileStmt):
        start_label = self.new_label()
        stop_label = self.new_label()
        self.emit(LabelIRInstruction(start_label))
        self.emit(
            BranchIRInstruction(
                left=self.build_expr(node.condition.left),
                right=self.build_expr(node.condition.right),
                op=invert_op_command(node.condition.op),
                label=stop_label
            )
        )
        for stmt in node.body_block.statements:
            self.build_stmt(stmt)
        self.emit(JumpIRInstruction(start_label))
        self.emit(LabelIRInstruction(stop_label))

    def build_if_stmt(self, node:IfStmt):
        else_label = self.new_label()
        end_label = self.new_label()
        self.emit(
            BranchIRInstruction(
                left=self.build_expr(node.condition.left),
                right=self.build_expr(node.condition.right),
                op=invert_op_command(node.condition.op),
                label=else_label
            )
        )
        for stmt in node.then_block.statements:
            self.build_stmt(stmt)
        self.emit(JumpIRInstruction(end_label))
        self.emit(LabelIRInstruction(else_label))
        if node.else_block.statements:
            for stmt in node.else_block.statements:
                self.build_stmt(stmt)
        self.emit(LabelIRInstruction(end_label))

    def build_stmt(self, node) -> None:
        logger.debug(f'Building statement for node: {node}')
        if isinstance(node, VarDecl):
            expr_temp: IRTemp = self.build_expr(node.expr)
            slot = self.get_slot(node.name)
            self.emit(StoreIRInstruction(src=expr_temp, dst=slot))
        elif isinstance(node, IfStmt):
            self.build_if_stmt(node)
        elif isinstance(node, WhileStmt):
            self.build_while_stmt(node)
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