from os import cpu_count
from typing import Dict, List

from backend.cpu_instr import ISACalcImm, ISACalcReg, ISAMemLoad, ISAMemStore, ISABranch
from backend.isa import Register, ALUOp, MemOp, BranchOp
from backend.labelalloc import LabelAllocator
from backend.regalloc import RegisterAllocator
from backend.temp_usage_analyzer import TempUsageAnalyzer
from ir import ProgrammIRInstruction, ConstIRInstruction, LoadIRInstruction, StoreIRInstruction, BinOpIRInstruction, PrintIRInstruction, IRTemp, IRConst

import logging

from ir.instructions import BranchIRInstruction, JumpIRInstruction, LabelIRInstruction

logger = logging.getLogger('Lowering')


class Lowerer:
    def __init__(self,
                 program: ProgrammIRInstruction):
        self.program = program
        self.register_allocator = RegisterAllocator()
        self.label_allocator = LabelAllocator()
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
        self.patch_offset()
        return self.cpu_instructions

    def patch_offset(self):
        logger.debug(f'Patching offset')
        logger.info(f'Label table: {self.label_allocator.labels}')
        for isa_instruction in self.cpu_instructions:
            if isinstance(isa_instruction, ISABranch):
                isa_instruction.imm = self.label_allocator.labels[isa_instruction.imm]

    def visit_instruction(self, instr):
        if isinstance(instr, ConstIRInstruction):
            self.visit_const(instr)
        elif isinstance(instr, LoadIRInstruction):
            self.visit_load(instr)
        elif isinstance(instr, StoreIRInstruction):
            self.visit_store(instr)
        elif isinstance(instr, BinOpIRInstruction):
            self.visit_binop(instr)
        elif isinstance(instr, BranchIRInstruction):
            self.visit_branch(instr)
        elif isinstance(instr, JumpIRInstruction):
            self.visit_jump(instr)
        elif isinstance(instr, LabelIRInstruction):
            self.visit_label(instr)
        else:
            raise Exception(f'Cant visit {instr}. Not implimented')

    def visit_label(self, label: LabelIRInstruction):
        self.label_allocator.labels[label.label.index] = len(self.cpu_instructions)*2

    def visit_branch(self, branch: BranchIRInstruction):
        left_reg = self.register_allocator.get_register(branch.left)
        right_reg = self.register_allocator.get_register(branch.right)
        op_map = {
        '==': BranchOp.BEQ,
        '!=': BranchOp.BNE,
        '>=': BranchOp.BGE,
        '<=': BranchOp.BLE,
        '<':  BranchOp.BGT,
        '>':  BranchOp.BLT
    }
        cpu_instr = ISABranch(
            rs1=left_reg,
            rs2=right_reg,
            op=op_map[branch.op],
            imm=branch.label.index
        )
        self.cpu_instructions.append(cpu_instr)

    def visit_jump(self, jump_ir: JumpIRInstruction):
        cpu_instr = ISABranch(
            op=BranchOp.JUMP,
            imm=jump_ir.label.index
        )
        self.cpu_instructions.append(cpu_instr)

    def visit_const(self, const_ir: ConstIRInstruction):
        reg: Register = self.register_allocator.allocate(const_ir.dst)
        cpu_instr = ISACalcImm(
            op=ALUOp.MOV,
            rd=reg,
            imm=const_ir.src.value
        )
        self.cpu_instructions.append(cpu_instr)

    def visit_load(self, load_ir: LoadIRInstruction):
        reg: Register = self.register_allocator.allocate(load_ir.dst)
        self.cpu_instructions.append(
            ISACalcImm(
                op=ALUOp.MOV,
                rd=Register.MAR,
                imm=load_ir.src.index
            )
        )
        self.cpu_instructions.append(
            ISAMemLoad(
                op=MemOp.LOAD,
                rd=reg
            )
        )

    def visit_store(self, store_ir: StoreIRInstruction):
        src_reg: Register = self.register_allocator.get_register(store_ir.src)
        self.cpu_instructions.append(
            ISACalcImm(
                op=ALUOp.MOV,
                rd=Register.MAR,
                imm=store_ir.dst.index
            )
        )
        self.cpu_instructions.append(
            ISAMemStore(
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
                ISACalcImm(
                    op=alu_op,
                    rs1=left_reg,
                    rd=dst_reg,
                    imm=binop_ir.right.value
                )
            )
        elif isinstance(binop_ir.right, IRTemp):
            right_reg = self.register_allocator.get_register(binop_ir.right)
            self.cpu_instructions.append(
                ISACalcReg(
                    op=alu_op,
                    rs1=left_reg,
                    rs2=right_reg,
                    rd=dst_reg
                )
            )
