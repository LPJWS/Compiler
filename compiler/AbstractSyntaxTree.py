from rply.token import BaseBox
from compiler.JSONparsedTree import Node
from compiler.errors import *
from llvmlite import ir


global_fmt = 1
fnctns = {}


class Program(BaseBox):
    def __init__(self, statement, program, state):
        self.state = state
        if type(program) is Program:
            self.statements = program.get_statements()
            self.statements.insert(0, statement)
        else:
            self.statements = [statement]

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def get_statements(self):
        return self.statements

    def eval(self, node):
        result = None
        for i, statement in enumerate(self.statements):
            left = Node('statement_full')
            right = Node('program')
            if i == len(self.statements) - 1:
                node.children.extend([left])
            else:
                node.children.extend([left, right])
            node = right
            result = statement.eval(left)
        return result


class Block(BaseBox):
    def __init__(self, statement, block, state, builder, module):
        self.state = state
        self.builder = builder
        self.module = module
        if type(block) is Block:
            self.statements = block.get_statements()
            self.statements.insert(0, statement)
        else:
            self.statements = [statement]

    def add_statement(self, statement):
        self.statements.insert(0, statement)

    def get_statements(self):
        return self.statements

    def eval(self, node):
        result = None
        for i, statement in enumerate(self.statements):
            left = Node('statement_full')
            right = Node('block')
            if i == len(self.statements) - 1:
                node.children.extend([left])
            else:
                node.children.extend([left, right])
            node = right

            result = statement.eval(left)
        return result


class If(BaseBox):
    def __init__(self, condition, body, builder, module, else_body=None, state=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body
        self.state = state
        self.builder = builder
        self.module = module

    def eval(self, node):
        expression = Node("expression")
        node.children.extend([Node("IF"), Node("("), expression, Node(")")])
        condition = self.condition.eval(expression)
        block = Node("block")
        node.children.extend([Node("{"), block, Node("}")])
        else_block = Node("block")

        if self.else_body is not None:
            with self.builder.if_else(condition) as (then, otherwise):
                with then:
                    self.body.eval(block)
                with otherwise:
                    self.else_body.eval(else_block)
        else:
            with self.builder.if_else(condition) as (then, otherwise):
                with then:
                    self.body.eval(block)
                with otherwise:
                    pass
        if self.else_body is not None:
            node.children.extend([Node("else"), Node("{"), else_block, Node("}")])
        # if bool(condition) is True:
        #     return self.body.eval(block)
        # else:
        #     if self.else_body is not None:
        #         return self.else_body.eval(else_block)
        return None


class While(BaseBox):
    def __init__(self, condition, body, builder, module, state=None):
        self.condition = condition
        self.body = body
        self.state = state
        self.builder = builder
        self.module = module

    def eval(self, node):
        expression = Node("expression")
        node.children.extend([Node("WHILE"), Node("("), expression, Node(")")])
        condition = self.condition.eval(expression)
        block = Node("block")
        node.children.extend([Node("{"), block, Node("}")])
        tmp = None

        while_block = self.builder.append_basic_block('while')
        self.state.while_body.append(while_block)
        while_block_end = self.builder.append_basic_block('while_end')
        self.state.while_end.append(while_block_end)

        self.builder.cbranch(condition, while_block, while_block_end)

        self.builder.position_at_end(while_block)
        self.body.eval(block)
        condition = self.condition.eval(expression)
        self.builder.cbranch(condition, while_block, while_block_end)

        self.builder.position_at_end(while_block_end)
        self.state.while_body.pop()
        self.state.while_end.pop()

        if bool(condition) is True:
            return tmp
        else:
            pass
        return None


class Break(BaseBox):
    def __init__(self, builder, module, state=None):
        self.state = state
        self.builder = builder
        self.module = module

    def eval(self, node):
        node.children.extend([Node("BREAK")])
        self.builder.branch(self.state.while_end[-1])


class Continue(BaseBox):
    def __init__(self, builder, module, state=None):
        self.state = state
        self.builder = builder
        self.module = module

    def eval(self, node):
        node.children.extend([Node("BREAK")])
        self.builder.branch(self.state.while_body[-1])


class Variable(BaseBox):
    def __init__(self, name, state, builder, module):
        self.name = str(name)
        self.value = None
        self.state = state
        self.builder = builder
        self.module = module

    def get_name(self):
        return str(self.name)

    def eval(self, node):
        identifier = Node("IDENTIFIER")
        node.children.extend([identifier])
        if dict(self.state.variables).get(self.name) is not None:
            self.value = self.state.variables[self.name]['value']
            identifier.children.extend([Node(self.name, [Node(self.value)])])
            i = self.builder.load(self.state.variables[self.name]['ptr'], self.name)
            return i
        identifier.children.extend([Node("Unknown name: <%s> is not defined" % str(self.name))])
        raise LogicError("Unknown name: <%s> is not defined" % str(self.name))

    def to_string(self):
        return str(self.name)


class FunctionDeclaration(BaseBox):
    def __init__(self, name, args, block, state):
        self.name = name
        self.args = args
        self.block = block
        state.functions[self.name] = self

    def eval(self, node):
        identifier = Node(self.name)
        node.children.extend([Node("FUNCTION"), identifier, Node("{"), Node("block"), Node("}")])
        return self

    def to_string(self):
        return "<function '%s'>" % self.name


class CallFunction(BaseBox):
    def __init__(self, name, args, state):
        self.name = name
        self.args = args
        self.state = state

    def eval(self, node):
        identifier = Node(self.name + " ( )")
        node.children.extend([identifier])
        return self.state.functions[self.name].block.eval(identifier)

    def to_string(self):
        return "<call '%s'>" % self.name


class BaseFunction(BaseBox):
    def __init__(self, expression, state):
        self.expression = expression
        self.value = None
        self.state = state
        self.roundOffDigits = 10

    def eval(self, node):
        raise NotImplementedError("This is abstract method from abstract class BaseFunction(BaseBox){...} !")

    def to_string(self):
        return str(self.value)


class Sumi(BaseFunction):
    def __init__(self, args, builder, module, state):
        super().__init__(args[0], state)
        self.expression2 = args[1]
        self.value2 = None
        self.builder = builder
        self.module = module

    def eval(self, node):
        expression = Node("expression")
        expression2 = Node("expression")
        node.children.extend([Node("CALLSUMI"), Node("("), expression, Node(","), expression2, Node(")")])
        self.value = self.expression.eval(expression)
        self.value2 = self.expression2.eval(expression2)

        res = self.builder.call(fnctns['sum'], (self.value, self.value2))
        return res


class Sumf(BaseFunction):
    def __init__(self, args, builder, module, state):
        super().__init__(args[0], state)
        self.expression2 = args[1]
        self.value2 = None
        self.builder = builder
        self.module = module

    def eval(self, node):
        expression = Node("expression")
        expression2 = Node("expression")
        node.children.extend([Node("CALLSUMF"), Node("("), expression, Node(","), expression2, Node(")")])
        self.value = self.expression.eval(expression)
        self.value2 = self.expression2.eval(expression2)

        res = self.builder.call(fnctns['sumf'], (self.value, self.value2))
        return res


class Constant(BaseBox):
    def __init__(self, state, builder, module):
        self.value = None
        self.state = state
        self.builder = builder
        self.module = module

    def eval(self, node):
        value = Node(self.value)
        typed = Node(self.__class__.__name__.upper(), [value])
        constant = Node("const", [typed])
        node.children.extend([constant])
        if self.__class__.__name__.upper() == 'INTEGER':
            i = ir.Constant(ir.IntType(8), int(self.value))
            return i
        elif self.__class__.__name__.upper() == 'FLOAT':
            i = ir.Constant(ir.FloatType(), float(self.value))
            return i
        return self.value

    def to_string(self):
        return str(self.value)


class Integer(Constant):
    def __init__(self, value, state, builder, module):
        super().__init__(state, builder, module)
        self.value = int(value)

    def to_string(self):
        return str(self.value)


class Float(Constant):
    def __init__(self, value, state, builder, module):
        super().__init__(state, builder, module)
        self.value = float(value)

    def to_string(self):
        return str(self.value)


class String(Constant):
    def __init__(self, value, state):
        super().__init__(state)
        self.value = str(value)

    def to_string(self):
        return '"%s"' % str(self.value)


class BinaryOp(BaseBox):
    def __init__(self, left, right, state, builder, module):
        self.left = left
        self.right = right
        self.state = state
        self.module = module
        self.builder = builder


class Assignment(BinaryOp):
    def __init__(self, left, right, state, builder, module, new=True, type_='INT'):
        super().__init__(left, right, state, builder, module)
        self.new = new
        self.type_ = type_

    def eval(self, node):
        if isinstance(self.left, Variable):
            var_name = self.left.get_name()
            types_dict = {ir.IntType(8): 'INT', ir.FloatType(): 'FLT', str: 'STR'}
            if self.new:
                if dict(self.state.variables).get(var_name) is None:
                    identifier = Node("IDENTIFIER", [Node(var_name)])
                    expression = Node("expression")
                    node.children.extend([Node("LET"), identifier, Node("="), expression])
                    tmp_eval = self.right.eval(expression)
                    if types_dict[tmp_eval.type] != self.type_:
                        raise LogicError('Cannot assign <%s> to <%s>-type variable' %
                                         (types_dict[type(tmp_eval)], self.type_))
                    alloc = self.builder.alloca(tmp_eval.type, size=None, name=var_name)
                    self.state.variables[var_name] = {'value': tmp_eval, 'type': self.type_, 'ptr': alloc}
                    self.builder.store(tmp_eval, alloc)
                    return self.state.variables
                else:
                    raise ImmutableError(var_name)
            else:
                if dict(self.state.variables).get(var_name) is not None:
                    identifier = Node("IDENTIFIER", [Node(var_name)])
                    expression = Node("expression")
                    node.children.extend([identifier, Node("="), expression])
                    tmp_eval = self.right.eval(expression)
                    # print(type(tmp_eval))
                    # if types_dict[type(tmp_eval)] != self.state.variables[var_name]['type']:
                    #     raise LogicError('Cannot assign <%s> to <%s>-type variable' %
                    #                      (types_dict[type(tmp_eval)], self.type_))
                    self.state.variables[var_name]['value'] = tmp_eval
                    alloc = self.state.variables[var_name]['ptr']
                    self.builder.store(tmp_eval, alloc)
                    return self.state.variables
                else:
                    raise LogicError("Variable <%s> is not defined" % var_name)

        else:
            raise LogicError("Cannot assign to <%s>" % self)


class Sum(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("+"), right])
        eval_left = self.left.eval(left)
        eval_right = self.right.eval(right)
        if eval_left.type == ir.FloatType():
            i = self.builder.fadd(eval_left, eval_right)
        else:
            i = self.builder.add(eval_left, eval_right)
        return i


class Sub(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("-"), right])
        eval_left = self.left.eval(left)
        eval_right = self.right.eval(right)
        if eval_left.type == ir.FloatType():
            i = self.builder.fsub(eval_left, eval_right)
        else:
            i = self.builder.sub(eval_left, eval_right)
        return i


class Mul(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("*"), right])
        eval_left = self.left.eval(left)
        eval_right = self.right.eval(right)
        if eval_left.type == ir.FloatType():
            i = self.builder.fmul(eval_left, eval_right)
        else:
            i = self.builder.mul(eval_left, eval_right)
        return i


class Div(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("/"), right])
        eval_left = self.left.eval(left)
        eval_right = self.right.eval(right)
        if eval_left.type == ir.FloatType():
            i = self.builder.fdiv(eval_left, eval_right)
        else:
            i = self.builder.sdiv(eval_left, eval_right)
        return i


class Equal(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("=="), right])
        eval_left = self.left.eval(left)
        eval_right = self.right.eval(right)
        if self.left.eval(left).type == ir.FloatType():
            i = self.builder.fcmp_ordered('==', eval_left, eval_right)
        else:
            i = self.builder.icmp_signed('==', eval_left, eval_right)
        return i


class NotEqual(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("!="), right])
        eval_left = self.left.eval(left)
        eval_right = self.right.eval(right)
        if self.left.eval(left).type == ir.FloatType():
            i = self.builder.fcmp_ordered('!=', eval_left, eval_right)
        else:
            i = self.builder.icmp_signed('!=', eval_left, eval_right)
        return i


class GreaterThan(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node(">"), right])
        eval_left = self.left.eval(left)
        eval_right = self.right.eval(right)
        if self.left.eval(left).type == ir.FloatType():
            i = self.builder.fcmp_ordered('>', eval_left, eval_right)
        else:
            i = self.builder.icmp_signed('>', eval_left, eval_right)
        return i


class LessThan(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("<"), right])
        eval_left = self.left.eval(left)
        eval_right = self.right.eval(right)
        if self.left.eval(left).type == ir.FloatType():
            i = self.builder.fcmp_ordered('<', eval_left, eval_right)
        else:
            i = self.builder.icmp_signed('<', eval_left, eval_right)
        return i


class GreaterThanEqual(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node(">="), right])
        eval_left = self.left.eval(left)
        eval_right = self.right.eval(right)
        if self.left.eval(left).type == ir.FloatType():
            i = self.builder.fcmp_ordered('>=', eval_left, eval_right)
        else:
            i = self.builder.icmp_signed('>=', eval_left, eval_right)
        return i


class LessThanEqual(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("<="), right])
        eval_left = self.left.eval(left)
        eval_right = self.right.eval(right)
        if self.left.eval(left).type == ir.FloatType():
            i = self.builder.fcmp_ordered('<=', eval_left, eval_right)
        else:
            i = self.builder.icmp_signed('<=', eval_left, eval_right)
        return i


class And(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("and"), right])
        left_eval = self.left.eval(left)
        right_eval = self.right.eval(right)
        i = self.builder.and_(left_eval, right_eval)
        return i


class Or(BinaryOp):
    def eval(self, node):
        left = Node("expression")
        right = Node("expression")
        node.children.extend([left, Node("or"), right])
        left_eval = self.left.eval(left)
        right_eval = self.right.eval(right)
        i = self.builder.or_(left_eval, right_eval)
        return i


class Not(BaseBox):
    def __init__(self, expression, state, builder, module):
        self.value = expression
        self.state = state
        self.builder = builder
        self.module = module

    def eval(self, node):
        expression = Node("expression")
        node.children.extend([Node("Not"), expression])
        self.value = self.value.eval(expression)
        i = self.builder.not_(self.value)
        return i


class Print(BaseBox):
    def __init__(self, builder, module, printf, expression=None, state=None):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.value = expression
        self.state = state

    def eval(self, node):
        node.children.extend([Node("PRINT"), Node("(")])
        if self.value is None:
            print()
        else:
            expression = Node("expression")
            node.children.extend([expression])
            value = self.value.eval(expression)

            voidptr_ty = ir.IntType(8).as_pointer()
            fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)

            self.builder.call(self.printf, [fmt_arg, value])
        node.children.extend([Node(")")])


class Input(BaseBox):
    def __init__(self, expression=None, state=None):
        self.value = expression
        self.state = state

    def eval(self, node):
        node.children.extend([Node("CONSOLE_INPUT"), Node("(")])
        if self.value is None:
            result = input()
        else:
            expression = Node("expression")
            node.children.extend([expression])
            result = input(self.value.eval(expression))
        node.children.extend([Node(")")])
        import re as regex
        if regex.search('^-?\d+(\.\d+)?$', str(result)):
            return float(result)
        else:
            return str(result)


class Main(BaseBox):
    def __init__(self, program, builder, module):
        global global_fmt
        self.program = program
        self.builder = builder
        self.module = module

        # import printf func
        fmt = "%i \n\0"
        c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(fmt)),
                            bytearray(fmt.encode("utf8")))
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt

        flt = ir.FloatType()
        int_ = ir.IntType(8)

        fnty = ir.FunctionType(int_, (int_, int_))
        func = ir.Function(self.module, fnty, name="sum")
        fnctns['sum'] = func
        block = func.append_basic_block(name="entry")
        f_builder = ir.IRBuilder(block)
        a, b = func.args
        result = f_builder.add(a, b, name="res")
        f_builder.ret(result)

        fnty = ir.FunctionType(flt, (flt, flt))
        func = ir.Function(self.module, fnty, name="fsum")
        fnctns['sumf'] = func
        block = func.append_basic_block(name="entry")
        f_builder = ir.IRBuilder(block)
        a, b = func.args
        result = f_builder.fadd(a, b, name="res")
        f_builder.ret(result)

    def eval(self, node):
        program = Node("program")
        node.children.extend([program])
        return self.program.eval(program)


class ExpressParenthesis(BaseBox):
    def __init__(self, expression):
        self.expression = expression

    def eval(self, node):
        expression = Node("expression")
        node.children.extend([Node("("), expression, Node(")")])
        return self.expression.eval(expression)


class StatementFull(BaseBox):
    def __init__(self, statement):
        self.statement = statement

    def eval(self, node):
        statement = Node("statement")
        node.children.extend([statement, Node(";")])
        return self.statement.eval(statement)


class Statement(BaseBox):
    def __init__(self, expression):
        self.expression = expression

    def eval(self, node):
        expression = Node("expression")
        node.children.extend([expression])
        return self.expression.eval(expression)
