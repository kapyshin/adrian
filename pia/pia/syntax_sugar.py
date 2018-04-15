from . import astlib, layers, defs
from .utils import A


def _e(expr):
    if expr in A(astlib.Call):
        expr.args = [e(arg) for arg in expr.args]
        return expr
    return expr


def _literal_to_struct_call(adr_type, py_type_name, args):
    return astlib.ModuleMember(
        astlib.Name(defs.PRELUDE),
        astlib.FuncCall(
            adr_type, [astlib.PyTypeCall(py_type_name, args)]))


def unsugar_literal(literal):
    if literal.type_ == astlib.LiteralT.number:
        return _literal_to_struct_call(
            astlib.Name(defs.NUMBER), astlib.Name(defs.INT), [literal])
    elif literal.type_ == astlib.LiteralT.string:
        return _literal_to_struct_call(
            astlib.Name(defs.STRING), astlib.Name(defs.STR), [literal])
    elif literal.type_ == astlib.LiteralT.vector:
        return _literal_to_struct_call(
            astlib.Name(defs.VECTOR), astlib.Name(defs.LIST), [astlib.Literal(
                literal.type_, [e(lit) for lit in literal.literal])])
    return literal


def e(expr):
    if expr in A(astlib.Literal):
        return unsugar_literal(expr)
    return _e(expr)


class SyntaxSugar(layers.Layer):

    def __init__(self):
        self.b = layers.b(SyntaxSugar)

    def decl(self, stmt):
        yield type(stmt)(stmt.name, stmt.type_, e(stmt.expr))

    @layers.register(astlib.VarDecl)
    def var_decl(self, stmt):
        yield from self.decl(stmt)

    @layers.register(astlib.LetDecl)
    def let_decl(self, stmt):
        yield from self.decl(stmt)

    @layers.register(astlib.Assignment)
    def assignment(self, stmt):
        yield astlib.Assignment(stmt.left, stmt.op, e(stmt.right))

    @layers.register(astlib.Return)
    def return_(self, stmt):
        yield astlib.Return(e(stmt.expr))

    @layers.register(astlib.FuncCall)
    def func_call(self, stmt):
        yield e(stmt)

    @layers.register(astlib.MethodCall)
    def method_call(self, stmt):
        yield e(stmt)

    def callable_decl(self, stmt):
        yield type(stmt)(
            stmt.name, stmt.args, stmt.rettype, self.b(stmt.body))

    @layers.register(astlib.FuncDecl)
    def func_decl(self, stmt):
        yield from self.callable_decl(stmt)

    @layers.register(astlib.StructFuncDecl)
    def struct_func_decl(self, stmt):
        yield from self.callable_decl(stmt)

    def data_decl(self, stmt):
        yield type(stmt)(
            stmt.name, stmt.parameters, stmt.protocols, self.b(stmt.body))

    @layers.register(astlib.StructDecl)
    def struct_decl(self, stmt):
        yield from self.data_decl(stmt)

    @layers.register(astlib.AdtDecl)
    def adt_decl(self, stmt):
        yield from self.data_decl(stmt)

    @layers.register(astlib.ProtocolDecl)
    def protocol_decl(self, stmt):
        yield from self.data_decl(stmt)
