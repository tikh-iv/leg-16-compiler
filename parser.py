from typing import List, Tuple
from ast_leg import VarDecl, BinaryOp, Number, VarRef, Program, Print, Stmt, Expr, Node
from lexer import Token

class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens: List[Token] = tokens
        self.pos: int = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def consume(self, expected_type):
        tok_type, value = self.peek()
        if tok_type != expected_type:
            raise SyntaxError(f'Token type {tok_type} is not expeted {expected_type}')
        self.pos += 1
        return value

    def parse_statement(self) -> Stmt:
        tok_type, _ = self.peek()

        if tok_type == 'VAR':
            return self.parse_var_decl()
        elif tok_type == 'PRINT':
            return self.parse_print()
        else:
            raise SyntaxError("Unknown statement")

    def parse_var_decl(self) -> VarDecl:
        self.consume('VAR')
        name = self.consume('IDENT')
        self.consume('ASSIGN')
        expr = self.parse_expr()
        self.consume('SEMI')
        return VarDecl(name, expr)

    def parse_print(self) -> Print:
        self.consume('PRINT')
        name = self.consume('IDENT')
        return Print(VarRef(name))

    def parse_expr(self) -> Expr:
        left = self.parse_term()

        if self.pos < len(self.tokens):
            tok_type, value = self.peek()
            if tok_type in ('PLUS', 'MINUS', 'MOD'):
                op = value
                self.pos += 1
                right = self.parse_term()
                return BinaryOp(left, op, right)

        return left

    def parse_term(self) -> Expr:
        tok_type, value = self.peek()

        if tok_type == 'NUMBER':
            self.pos += 1
            return Number(int(value))

        elif tok_type == 'IDENT':
            self.pos += 1
            return VarRef(value)

        else:
            raise SyntaxError("Expected number or identifier")
        
    def parse_program(self) -> Program:
        stmts = []
        while self.pos < len(self.tokens):
            stmts.append(self.parse_statement())
        return Program(stmts)
