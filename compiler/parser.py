from rply import ParserGenerator
from compiler.JSONparsedTree import Node
from compiler.AbstractSyntaxTree import *
from compiler.errors import *


class ParserState(object):
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.while_body = []
        self.while_end = []


class Parser:
    def __init__(self, module, builder, printf, syntax=False):
        self.pg = ParserGenerator(
            ['INTEGER', 'FLOAT',
             '(', ')', ',', ';', '{', '}',
             'AND', 'OR', 'NOT',
             'IF', 'ELSE',
             'WHILE', 'BREAK', 'CONTINUE',
             'INT', 'FLT',
             '=', '==', '!=', '>=', '>', '<', '<=',
             'SUM', 'SUB', 'MUL', 'DIV', 'IDENTIFIER', 'FUNCTION',
             'SUMI', 'SUMF', 'PRINT',
             ],
            precedence=(
                ('left', ['FUNCTION']),
                ('left', ['LET']),
                ('left', ['=']),
                ('left', ['IF', 'ELSE', ';']),
                ('left', ['AND', 'OR']),
                ('left', ['NOT']),
                ('left', ['==', '!=', '>=', '>', '<', '<=']),
                ('left', ['SUM', 'SUB']),
                ('left', ['MUL', 'DIV']),
                ('left', ['STRING', 'INTEGER', 'FLOAT', 'BOOLEAN'])
            )
        )
        self.builder = builder
        self.module = module
        self.printf = printf
        self.syntax = syntax
        self.parse()

    def parse(self):

        @self.pg.production("main : program")
        def main_program(state, p):
            if self.syntax is True:
                return [Node("program", p[0])]
            return Main(p[0], self.builder, self.module)

        @self.pg.production('program : statement_full')
        def program_statement(state, p):
            if self.syntax is True:
                return [Node("statement_full", p[0])]
            return Program(p[0], None, state)

        @self.pg.production('program : statement_full program')
        def program_statement_program(state, p):
            if self.syntax is True:
                return [Node("statement_full", p[0]), Node("program", p[1])]
            return Program(p[0], p[1], state)

        @self.pg.production('expression : ( expression )')
        def expression_parenthesis(state, p):
            if self.syntax is True:
                return [Node("("), Node("expression", p[1]), Node(")")]
            return ExpressParenthesis(p[1])

        @self.pg.production('statement_full : IF ( expression ) { block }')
        def expression_if(state, p):
            if self.syntax is True:
                return [Node("IF"), Node("("), Node("expression", p[2]), Node(")"), Node("{"), Node("block", p[5]), Node("}")]
            return If(p[2], p[5], self.builder, self.module, state=state)

        @self.pg.production('statement_full : IF ( expression ) { block } ELSE { block }')
        def expression_if_else(state, p):
            if self.syntax is True:
                return [Node("IF"), Node("("), Node("expression", p[2]), Node(")"), Node("{"), Node("block", p[5]), Node("}"), Node("ELSE"), Node("{"),
                        Node("block", p[9]), Node("}")]
            return If(p[2], p[5], self.builder, self.module, else_body=p[9], state=state)

        @self.pg.production('block : statement_full')
        def block_expr(state, p):
            if self.syntax is True:
                return [Node("statement_full", p[0])]
            return Block(p[0], None, state, self.builder, self.module)

        @self.pg.production('block : statement_full block')
        def block_expr_block(state, p):
            if self.syntax is True:
                return [Node("statement_full", p[0]), Node("block", p[1])]
            return Block(p[0], p[1], state, self.builder, self.module)

        @self.pg.production('statement_full : WHILE ( expression ) { block }')
        def expression_while(state, p):
            if self.syntax is True:
                return [Node("WHILE"), Node("("), Node("expression", p[2]), Node(")"), Node("{"), Node("block", p[5]),
                        Node("}")]
            return While(p[2], p[5], self.builder, self.module, state=state)

        @self.pg.production('statement_full : statement ;')
        def statement_full(state, p):
            if self.syntax is True:
                return [Node("statement", p[0]), Node(";")]
            return StatementFull(p[0])

        @self.pg.production('statement : expression')
        def statement_expr(state, p):
            if self.syntax is True:
                return [Node("expression", p[0])]
            return Statement(p[0])

        @self.pg.production('statement : BREAK')
        def statement_break(state, p):
            if self.syntax is True:
                return [Node("BREAK", p[0])]
            return Break(self.builder, self.module, state=state)

        @self.pg.production('statement : CONTINUE')
        def statement_continue(state, p):
            if self.syntax is True:
                return [Node("CONTINUE", p[0])]
            return Continue(self.builder, self.module, state=state)

        @self.pg.production('statement : INT IDENTIFIER = expression')
        @self.pg.production('statement : FLT IDENTIFIER = expression')
        def statement_assignment_type(state, p):
            if p[0].gettokentype() == 'INT':
                if self.syntax is True:
                    return [Node("INT"), Node("IDENTIFIER", p[1]), Node("="), Node("expression", p[3])]
            elif p[0].gettokentype() == 'FLT':
                if self.syntax is True:
                    return [Node("FLT"), Node("IDENTIFIER", p[1]), Node("="), Node("expression", p[3])]
            return Assignment(Variable(p[1].getstr(), state, self.builder, self.module), p[3], state, self.builder, self.module, type_=p[0].gettokentype())

        @self.pg.production('statement : IDENTIFIER = expression')
        def statement_assignment(state, p):
            if self.syntax is True:
                return [Node("IDENTIFIER", p[0]), Node("="), Node("expression", p[2])]
            return Assignment(Variable(p[0].getstr(), state, self.builder, self.module), p[2], state, self.builder, self.module, new=False)

        @self.pg.production('statement_full : FUNCTION IDENTIFIER ( ) { block }')
        def statement_func_noargs(state, p):
            if self.syntax is True:
                return [Node("FUNCTION"), Node("IDENTIFIER", p[1]), Node("("), Node(")"), Node("{"), Node("block", p[5]), Node("}")]
            return FunctionDeclaration(name=p[1].getstr(), args=None, block=p[5], state=state)

        @self.pg.production('expression : NOT expression')
        def expression_not(state, p):
            if self.syntax is True:
                return [Node("NOT"), Node("expression", p[1])]
            return Not(p[1], state, self.builder, self.module)

        @self.pg.production('expression : expression SUM expression')
        @self.pg.production('expression : expression SUB expression')
        @self.pg.production('expression : expression MUL expression')
        @self.pg.production('expression : expression DIV expression')
        def expression_binary_operator(state, p):
            if p[1].gettokentype() == 'SUM':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("+"), Node("expression", p[2])]
                return Sum(p[0], p[2], state, self.builder, self.module)
            elif p[1].gettokentype() == 'SUB':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("-"), Node("expression", p[2])]
                return Sub(p[0], p[2], state, self.builder, self.module)
            elif p[1].gettokentype() == 'MUL':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("*"), Node("expression", p[2])]
                return Mul(p[0], p[2], state, self.builder, self.module)
            elif p[1].gettokentype() == 'DIV':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("/"), Node("expression", p[2])]
                return Div(p[0], p[2], state, self.builder, self.module)
            else:
                raise LogicError('Unknown operator: %s' % p[1].gettokentype())

        @self.pg.production('expression : expression != expression')
        @self.pg.production('expression : expression == expression')
        @self.pg.production('expression : expression >= expression')
        @self.pg.production('expression : expression <= expression')
        @self.pg.production('expression : expression > expression')
        @self.pg.production('expression : expression < expression')
        @self.pg.production('expression : expression AND expression')
        @self.pg.production('expression : expression OR expression')
        def expression_equality(state, p):
            if p[1].gettokentype() == '==':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("=="), Node("expression", p[2])]
                return Equal(p[0], p[2], state, self.builder, self.module)
            elif p[1].gettokentype() == '!=':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("!="), Node("expression", p[2])]
                return NotEqual(p[0], p[2], state, self.builder, self.module)
            elif p[1].gettokentype() == '>=':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node(">="), Node("expression", p[2])]
                return GreaterThanEqual(p[0], p[2], state, self.builder, self.module)
            elif p[1].gettokentype() == '<=':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("<="), Node("expression", p[2])]
                return LessThanEqual(p[0], p[2], state, self.builder, self.module)
            elif p[1].gettokentype() == '>':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node(">"), Node("expression", p[2])]
                return GreaterThan(p[0], p[2], state, self.builder, self.module)
            elif p[1].gettokentype() == '<':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("<"), Node("expression", p[2])]
                return LessThan(p[0], p[2], state, self.builder, self.module)
            elif p[1].gettokentype() == 'AND':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("AND"), Node("expression", p[2])]
                return And(p[0], p[2], state, self.builder, self.module)
            elif p[1].gettokentype() == 'OR':
                if self.syntax is True:
                    return [Node("expression", p[0]), Node("OR"), Node("expression", p[2])]
                return Or(p[0], p[2], state, self.builder, self.module)
            else:
                raise LogicError("Unknown operator: %s" % p[1].gettokentype())

        @self.pg.production('statement : PRINT ( )')
        def program(state, p):
            if self.syntax is True:
                return [Node("PRINT"), Node("("), Node(")")]
            return Print(self.builder, self.module, self.printf)

        @self.pg.production('statement : PRINT ( expression )')
        def program(state, p):
            if self.syntax is True:
                return [Node("PRINT"), Node("("), Node("expression", p[2]), Node(")")]
            return Print(self.builder, self.module, self.printf, expression=p[2], state=state)

        @self.pg.production('expression : IDENTIFIER')
        def expression_variable(state, p):
            if self.syntax is True:
                return [Node("IDENTIFIER", p[0].getstr())]
            return Variable(p[0].getstr(), state, self.builder, self.module)

        @self.pg.production('expression : IDENTIFIER ( )')
        def expression_call_noargs(state, p):
            if self.syntax is True:
                return [Node("IDENTIFIER", p[0]), Node("("), Node(")")]
            return CallFunction(name=p[0].getstr(), args=None, state=state)

        @self.pg.production('expression : SUMI ( expression , expression )')
        def expression_call(state, p):
            if self.syntax is True:
                return [Node("IDENTIFIER", p[0]), Node("("), Node(")")]
            return Sumi((p[2], p[4]), self.builder, self.module, state=state)

        @self.pg.production('expression : SUMF ( expression , expression )')
        def expression_call(state, p):
            if self.syntax is True:
                return [Node("IDENTIFIER", p[0]), Node("("), Node(")")]
            return Sumf((p[2], p[4]), self.builder, self.module, state=state)

        @self.pg.production('expression : const')
        def expression_const(state, p):
            if self.syntax is True:
                return [Node("const", p[0])]
            return p[0]

        @self.pg.production('const : FLOAT')
        def constant_float(state, p):
            if self.syntax is True:
                return [Node("FLOAT", p[0])]
            return Float(p[0].getstr(), state, self.builder, self.module)

        @self.pg.production('const : INTEGER')
        def constant_integer(state, p):
            if self.syntax is True:
                return [Node("INTEGER", p[0])]
            return Integer(p[0].getstr(), state, self.builder, self.module)

        @self.pg.error
        def error_handle(state, token):
            raise ValueError(token)

    def build(self):
        return self.pg.build()
