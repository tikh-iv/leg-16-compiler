from __future__ import annotations

from typing import List
from frontend.ast_leg import VarDecl, BinaryOp, Number, VarRef, Program, Print, Stmt, Expr, IfStmt, Block, WhileStmt
from ir.builder import logger
from frontend.lexer import Token

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
        logger.debug(f'Parsing statement {tok_type}')

        if tok_type == 'VAR':
            return self.parse_var_decl()
        elif tok_type == 'PRINT':
            return self.parse_print()
        elif tok_type == 'IF':
            return  self.parse_if()
        elif tok_type == 'WHILE':
            return self.parse_while()
        else:
            raise SyntaxError("Unknown statement")

    def parse_block(self) -> Block:
        statements = []
        self.consume('LBRACE')
        tok_type = ''
        while tok_type != 'RBRACE':
            statements.append(self.parse_statement())
            tok_type, value = self.peek()
        self.consume('RBRACE')
        logger.debug(f'Parced block {statements}')
        return Block(statements=statements)

    def parse_if(self) -> IfStmt:
        self.consume('IF')
        condition = self.parse_expr()
        logger.debug(f'Parced if condition {condition}')
        self.consume('COLON')
        block = self.parse_block()
        logger.debug(f'Parced if block {block}')
        tok_type, value = self.peek()
        if tok_type == 'ELSE':
            self.consume('ELSE')
            else_block = self.parse_block()
        else:
            else_block = Block([])
        logger.debug(f'Parced else block {block}')
        return IfStmt(condition, block, else_block)

    def parse_while(self) -> WhileStmt:
        self.consume('WHILE')
        condition = self.parse_expr()
        logger.debug(f'Parced While condition {condition}')
        self.consume('COLON')
        block = self.parse_block()
        logger.debug(f'Parced While block {block}')
        return WhileStmt(condition, block)

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

    def parse_expr(self) -> Expr | BinaryOp:
        left = self.parse_term()
        while self.pos < len(self.tokens):
            tok_type, value = self.peek()
            if tok_type in (
                'PLUS', 'MINUS', 'MOD', 'MUL','DIV',
                'AND', 'OR', 'XOR', 'SHL', 'SHR', 'ROL', 'ROR',
                'GT', 'LT', 'GE', 'LE', 'EQ', 'NE'
            ):
                op = value
                self.pos += 1
                right = self.parse_term()
                left = BinaryOp(left, op, right)
            else:
                break
        return left

    def parse_term(self) -> Expr:
        tok_type, value = self.peek()

        if tok_type == 'NOT':
            self.pos += 1
            expr = self.parse_term()
            return BinaryOp(Number(0), value, expr)

        if tok_type == 'NUMBER':
            self.pos += 1
            return Number(int(value))

        elif tok_type == 'IDENT':
            self.pos += 1
            return VarRef(value)

        elif tok_type in ('MUL', 'DIV'):
            raise SyntaxError("Binary operator without left operand")

        else:
            raise SyntaxError("Expected number or identifier")

    def parse_program(self) -> Program:
        stmts = []
        while self.peek()[0] != 'EOF':
            logger.debug(f'Parsing program from token {self.peek()}')
            stmts.append(self.parse_statement())
        return Program(stmts)
