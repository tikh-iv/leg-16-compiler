import re
from typing import List, Tuple

Token = Tuple[str, str]  # (type, value)

class Lexer:
    token_specification = [
        ('SKIP', r'[ \t\n]+'),  # Skip spaces
        ('COMMENT', r'//.*'),  # Comments

        ('SEMI', r';'),
        ('ASSIGN', r'='),

        ('SHL', r'<<'),
        ('SHR', r'>>'),

        ('PLUS', r'\+'),
        ('MINUS', r'-'),
        ('MUL', r'\*'),
        ('DIV', r'/'),
        ('MOD', r'%'),

        ('AND', r'&'),
        ('OR', r'\|'),
        ('XOR', r'\^'),
        ('NOT', r'~'),

        ('ROL', r'\brol\b'),
        ('ROR', r'\bror\b'),

        ('PRINT', r'\bprint\b'),
        ('VAR', r'\bvar\b'),

        ('NUMBER', r'\d+'),
        ('IDENT', r'[a-zA-Z_]\w*'),

        ('MISMATCH', r'.'),  # Mismatch is error
    ]
    # Pattern generator use to create big regexp pattern, like r'(?P<SKIP>[ \\t\\n]+)|(?P<COMMENT>//.*)|(?
    master_pattern = re.compile('|'.join(f'(?P<{name}>{pat})' for name, pat in token_specification))

    def __init__(self,
                 code: str) -> None:
        self.code = code.strip()

    def tokenize(self) -> List[Token]:
        lex_tokens = []
        line_no = 1
        line_start = 0
        # self.master_pattern.finditer(self.code) is iterator with found items
        for mo in self.master_pattern.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'SKIP':
                # Считаем переводы строк для лучшей диагностики ошибок
                line_no += value.count('\n')
                continue
            elif kind == 'COMMENT':
                continue
            elif kind == 'MISMATCH':
                column = mo.start() - line_start + 1
                raise RuntimeError(f'Unexpected symbol {value!r} string {line_no}, column {column}')
            else:
                lex_tokens.append((kind, value))
                if '\n' in value:
                    line_no += value.count('\n')
                    line_start = mo.end() - value.rfind('\n') - 1
        return lex_tokens
