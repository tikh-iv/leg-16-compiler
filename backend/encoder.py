from typing import List

from backend.cpu_instr import ISAInstruction


class Encoder:
    def encode(self, instr: ISAInstruction):
        word = (
            (instr.dec_op << 13) |
            (instr.op << 9) |
            (instr.rs1 << 6) |
            (instr.rs2 << 3) |
            (instr.rd << 0)
        )
        return word, instr.imm

    def encode_program(self, lowered_program: List):
        encoded_program = []
        for command in lowered_program:
             encoded_program.append(self.encode(command))
        return encoded_program