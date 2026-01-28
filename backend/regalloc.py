from typing import List, Dict

from isa import Register
from ir import IRTemp

import logging
logger = logging.getLogger('Allocator')


class RegisterAllocator:
    def __init__(self):
        self.all_registers: List[Register] = [
            Register.R0,
            Register.R1,
            Register.R2,
            Register.R3,
            Register.R4,
            Register.R5
        ]
        self.free_registers: List[Register] = list(self.all_registers)
        self.temp_to_reg: Dict[int, Register] = {}
        self.reg_to_temp: Dict[Register, int] = {}
        self.refcount: Dict[int, int] = {}

    def reset(self):
        logger.info('Resetting registers')
        self.free_registers: List[Register] = list(self.all_registers)
        self.temp_to_reg: Dict[int, Register] = {}
        self.reg_to_temp: Dict[Register, int] = {}
        self.refcount: Dict[int, int] = {}

    def allocate(self, temp_ir: IRTemp):
        logger.debug(f'Allocating register for temp {temp_ir}')
        if self.is_allocated(temp_ir):
            raise Exception(f'Cannot allocate, temp is already allocated.')
        else:
            if self.free_registers:
                reg_to_allocate = self.free_registers.pop()
                self.temp_to_reg[temp_ir.id] = reg_to_allocate
                self.reg_to_temp[reg_to_allocate] = temp_ir.id
                logger.debug(f'Allocated register {reg_to_allocate}')
            else:
                raise Exception(f'There is no free registers. Cannot allocate.')
        logger.info(f'For temp_id {temp_ir} register {self.temp_to_reg[temp_ir.id]} was allocated.')
        return self.temp_to_reg[temp_ir.id]

    def free(self, temp_ir: IRTemp):
        logger.debug(f'Free register for temp {temp_ir}')
        if self.is_allocated(temp_ir):
            reg_for_free = self.temp_to_reg[temp_ir.id]
            self.reg_to_temp.pop(reg_for_free)
            self.temp_to_reg.pop(temp_ir.id)
            self.free_registers.append(reg_for_free)
            logger.info(f'Free register {reg_for_free} was free.')
        else:
            raise Exception(f'This temp is no allocated. Cannot free.')

    def set_refcount(self, refcount: Dict[int,int]):
        self.refcount = refcount

    def consume(self, temp_ir: IRTemp):
        logger.debug(f'Consume register for temp {temp_ir}')
        if self.is_allocated(temp_ir):
            self.refcount[temp_ir.id] -= 1
            if self.refcount[temp_ir.id] == 0:
                self.free(temp_ir)
        else:
            raise Exception(f'This temp is no allocated. Cannot consume.')

    def is_allocated(self, temp_ir: IRTemp):
        if self.temp_to_reg.get(temp_ir.id, None) is not None:
            return True
        else:
            return False

    def get(self, temp_ir: IRTemp):
        logger.debug(f'Get register for temp {temp_ir}')
        if self.is_allocated(temp_ir):
            logger.info(f'Get register for temp {temp_ir} was allocated.')
            return self.temp_to_reg[temp_ir.id]
        else:
            raise Exception(f'Register is not allocated.')