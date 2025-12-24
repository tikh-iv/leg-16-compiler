from lexer import Lexer

code = """
var a = 10;
var b = 16;
var c = a % b;
print c;
"""

lexer = Lexer(code)
tokens = lexer.tokenize()

for tok_type, tok_value in tokens:
    print(f'{tok_type:8} | {tok_value}')