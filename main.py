from typing import List, Tuple
from lexer import Lexer, Token
from parser import Parser


code = """
var a = 10;
var b = 16;
var c = a % b;
print c
"""

lexer = Lexer(code)
tokens: List[Token] = lexer.tokenize()

for tok_type, tok_value in tokens:
    print(f'{tok_type:8} | {tok_value}')

leg_parser = Parser(tokens)
ast = leg_parser.parse_program()
print(ast)