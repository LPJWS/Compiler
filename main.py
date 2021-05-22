from compiler.lexer import Lexer
from compiler.parser import Parser, ParserState
from compiler.JSONparsedTree import Node, write
from compiler.codegen import CodeGen
from rply.lexer import LexerStream
from copy import copy
from pprint import pprint
import traceback
import json

input_file = open('input.code').read()

lexer = Lexer().build()
tokens: LexerStream
try:
    tokens = lexer.lex(input_file)
    tokenType = map(lambda x: x.gettokentype(), copy(tokens))
    tokenName = map(lambda x: x.getstr(), copy(tokens))
    pprint(list(copy(tokens)))
except (BaseException, Exception):
    traceback.print_exc()
finally:
    print("\n\nResult:")

codegen = CodeGen()
module = codegen.module
builder = codegen.builder
printf = codegen.printf

SymbolTable = ParserState()
syntaxRoot: Node
semanticRoot = Node("main")
try:
    syntaxRoot = Node("main", Parser(module, builder, printf, syntax=True).build().parse(copy(tokens), state=SymbolTable))
    Parser(module, builder, printf).build().parse(copy(tokens), state=SymbolTable).eval(semanticRoot)
except (BaseException, Exception):
    traceback.print_exc()
finally:
    write(syntaxRoot, "SyntaxAnalyzer")
    write(semanticRoot, "SemanticAnalyzer")

    codegen.create_ir()
    codegen.save_ir("output.ll")

    print('End of program')
    print("\n\nSymbol table:")
    for v in SymbolTable.variables.keys():
        print('%s | %s | %s' % (v, SymbolTable.variables[v]['type'], SymbolTable.variables[v]['value']))
    for v in SymbolTable.functions.keys():
        print('%s | func | %s' % (v, SymbolTable.functions[v]))

    # with open('treant-js-master/SemanticAnalyzer.json', 'r') as file:
    #     print(json.dumps(json.loads(file.read()), sort_keys=False, indent=4))
