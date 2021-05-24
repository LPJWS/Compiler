from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()
        self.__add_tokens()

    def __add_tokens(self):
        # Types
        self.lexer.add('FLOAT', r'-?\d+\.\d+')
        self.lexer.add('INTEGER', r'-?\d+')
        # Mathematical Operators
        self.lexer.add('SUM', r'\+')
        self.lexer.add('SUB', r'\-')
        self.lexer.add('MUL', r'\*')
        self.lexer.add('DIV', r'\/')
        # Binary Operator
        self.lexer.add('AND', r'and(?!\w)')
        self.lexer.add('OR', r'or(?!\w)')
        self.lexer.add('==', r'\=\=')
        self.lexer.add('!=', r'\!\=')
        self.lexer.add('>=', r'\>\=')
        self.lexer.add('<=', r'\<\=')
        self.lexer.add('>', r'\>')
        self.lexer.add('<', r'\<')
        self.lexer.add('=', r'\=')
        # Statement
        self.lexer.add('IF', r'if(?!\w)')
        self.lexer.add('ELSE', r'else(?!\w)')
        self.lexer.add('NOT', r'not(?!\w)')
        self.lexer.add('WHILE', r'while(?!\w)')
        self.lexer.add('BREAK', r'break(?!\w)')
        self.lexer.add('CONTINUE', r'continue(?!\w)')
        # Semi Colon
        self.lexer.add(';', r'\;')
        self.lexer.add(',', r'\,')
        # Parenthesis
        self.lexer.add('(', r'\(')
        self.lexer.add(')', r'\)')
        self.lexer.add('{', r'\{')
        self.lexer.add('}', r'\}')
        # Function
        self.lexer.add('PRINT', r'print')
        self.lexer.add('SUMI', r'sum(?!\w)')
        self.lexer.add('SUMF', r'sumf(?!\w)')
        self.lexer.add('SUBI', r'sub(?!\w)')
        self.lexer.add('SUBF', r'subf(?!\w)')
        self.lexer.add('FUNC', r'def(?!\w)')
        self.lexer.add('RETURN', r'return(?!\w)')
        # Assignment
        self.lexer.add('INT', r'int(?!\w)')
        self.lexer.add('FLT', r'float(?!\w)')
        self.lexer.add('IDENTIFIER', "[a-zA-Z_][a-zA-Z0-9_]*")
        # Ignore spaces
        self.lexer.ignore('\/\/.*')
        self.lexer.ignore('\/[*](.|\n)*[*]\/')
        self.lexer.ignore('\s+')

    def build(self):
        return self.lexer.build()
