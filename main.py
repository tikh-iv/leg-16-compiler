from typing import List, Tuple
from lexer import Lexer, Token
from parser import Parser
from symbol_table import SemanticAnalyzer, SymbolTable
from ast_leg import Node, Expr, Program
from ir.builder import IRBuilder

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:%(name)s:%(message)s'
)



code = """
var a = 10;
var b = 16;
var c = a % b;
print c
var aaa = b;
var ccc = 777;
var bbb = aaa % ccc;
"""

lexer = Lexer(code)
tokens: List[Token] = lexer.tokenize()

for tok_type, tok_value in tokens:
    print(f'{tok_type:8} | {tok_value}')

leg_parser = Parser(tokens)
leg_ast: Program = leg_parser.parse_program()
print(leg_ast)

analyzer = SemanticAnalyzer()
analyzer.visit(leg_ast)
print(analyzer.table.symbols)

builder = IRBuilder(symbol_table=analyzer.table)
ir_program = builder.build_program(leg_ast)
print(ir_program)


import pprint
pprint.pprint(ir_program.instructions) 
pprint.pprint(ir_program.slots)