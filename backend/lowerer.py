from os import cpu_count
from typing import Dict, List

from backend.cpu_instr import CalcImm, CalcReg, MemLoad, MemStore
from backend.isa import Register, ALUOp, MemOp
from backend.regalloc import RegisterAllocator
from backend.temp_usage_analyzer import TempUsageAnalyzer
from ir import ProgrammIRInstruction, ConstIRInstruction, LoadIRInstruction, StoreIRInstruction, BinOpIRInstruction, PrintIRInstruction, IRTemp, IRConst

import logging
logger = logging.getLogger('Lowering')


class Lowerer:
    def __init__(self,
                 program: ProgrammIRInstruction,
                 register_allocator: RegisterAllocator):
        self.program = program
        self.register_allocator = register_allocator
        self.refcount = {}
        self.cpu_instructions: List = []
        self.temp_usage_analyzer = TempUsageAnalyzer(self.program)

    def lower(self):
        logger.info(f'Lowering program')
        self.refcount = self.temp_usage_analyzer.analyze()
        self.register_allocator.set_refcount(self.refcount)
        for instr in self.program.instructions:
            logger.debug(f'Lowering instruction {instr}')
            self.visit_instruction(instr)
            for temp in instr.used_temps():
                self.register_allocator.consume(temp)
        return self.cpu_instructions

    def visit_instruction(self, instr):
        if isinstance(instr, ConstIRInstruction):
            cpu_instr = self.visit_const(instr)
        elif isinstance(instr, LoadIRInstruction):
            cpu_instr = self.visit_load(instr)
        elif isinstance(instr, StoreIRInstruction):
            cpu_instr = self.visit_store(instr)
        elif isinstance(instr, BinOpIRInstruction):
            cpu_instr = self.visit_binop(instr)
        elif isinstance(instr, PrintIRInstruction):
            cpu_count = None

    def visit_const(self, const_ir: ConstIRInstruction):
        reg: Register = self.register_allocator.allocate(const_ir.dst)
        cpu_instr = CalcImm(
            op=ALUOp.MOV,
            rs1=Register.R0, # заглушка
            rd=reg,
            imm=const_ir.src.value
        )
        self.cpu_instructions.append(cpu_instr)

    def visit_load(self, load_ir: LoadIRInstruction):
        reg: Register = self.register_allocator.allocate(load_ir.dst)
        self.cpu_instructions.append(
            CalcImm(
                op=ALUOp.MOV,
                rs1=Register.R0,  # заглушка
                rd=Register.MAR,
                imm=load_ir.src.index
            )
        )
        self.cpu_instructions.append(
            MemLoad(
                op=MemOp.LOAD,
                rd=reg
            )
        )

    def visit_store(self, store_ir: StoreIRInstruction):
        src_reg: Register = self.register_allocator.get_register(store_ir.src)
        self.cpu_instructions.append(
            CalcImm(
                op=ALUOp.MOV,
                rd=Register.MAR,
                imm=store_ir.dst.index
            )
        )
        self.cpu_instructions.append(
            MemStore(
                op=MemOp.STOR,
                rs1=src_reg
            )
        )


    def visit_binop(self, binop_ir: BinOpIRInstruction):
        # Map string operations to ALUOp
        op_map = {
            '+': ALUOp.ADD,
            '-': ALUOp.SUB,
            '*': ALUOp.MUL,
            '/': ALUOp.DIV,
            '&': ALUOp.AND,
            '|': ALUOp.OR,
            '^': ALUOp.XOR,
            '<<': ALUOp.SHL,
            '>>': ALUOp.SHR,
            '%': ALUOp.DIVH
        }
        
        alu_op = op_map.get(binop_ir.op, ALUOp.ADD)  # Default to ADD if op not found
        dst_reg: Register = self.register_allocator.allocate(binop_ir.dst)
        
        # Check if we can use immediate mode
        left_reg = self.register_allocator.get_register(binop_ir.left)

        if isinstance(binop_ir.right, IRConst):
            self.cpu_instructions.append(
                CalcImm(
                    op=alu_op,
                    rs1=left_reg,
                    rd=dst_reg,
                    imm=binop_ir.right.value
                )
            )
        elif isinstance(binop_ir.right, IRTemp):
            right_reg = self.register_allocator.get_register(binop_ir.right)
            self.cpu_instructions.append(
                CalcReg(
                    op=alu_op,
                    rs1=left_reg,
                    rs2=right_reg,
                    rd=dst_reg
                )
            )
