from typing import List

from backend.encoder import Encoder
from backend.lowerer import Lowerer
from backend.regalloc import RegisterAllocator
from frontend.lexer import Lexer, Token
from frontend.parser import Parser
from frontend.symbol_table import SemanticAnalyzer
from frontend.ast_leg import Program
from ir.builder import IRBuilder

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(name)s:%(message)s'
)



code = """
var a = 2;
var b = 10;
while a < b:{
  var a = a + 1;
}
var c = a;
"""

lexer = Lexer(code)
tokens: List[Token] = lexer.tokenize()
print('tokens'+'-'*10)
for tok_type, tok_value in tokens:
    print(f'{tok_type:8} | {tok_value}')

leg_parser = Parser(tokens)
leg_ast: Program = leg_parser.parse_program()
print('leg_ast'+'-'*10)
print(leg_ast)

analyzer = SemanticAnalyzer()
analyzer.visit(leg_ast)
print('symbol_table'+'-'*10)
print(analyzer.table.symbols)

builder = IRBuilder(symbol_table=analyzer.table)
ir_program = builder.build_program(leg_ast)
print('ir_program'+'-'*10)
print(ir_program)

lowerer = Lowerer(ir_program)
lowered_program = lowerer.lower()

import pprint
pprint.pprint(ir_program.instructions) 
pprint.pprint(ir_program.slots)

print('-------'*10)

pprint.pprint(lowered_program)

print('-------'*10)
encoder = Encoder()
code = encoder.encode_program(lowered_program=lowered_program)


for word in code:
    print(f'{word[0]} {word[1]}')


for word in code:
    s = f'{word[0]:016b}'
    print(f'{s[:3]} {s[3:7]} {s[7:10]} {s[10:13]} {s[13:]} {word[1]}')