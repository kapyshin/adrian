import itertools

from . import layers, astlib, errors, defs, inference, heapify
from .context import (
    context, get, add_to_env, add_scope, del_scope)
from .patterns import A


def e(expr, name):
    if expr in A(
            astlib.CTYPES + (
            astlib.Expr, astlib.StructMember)):
        return heapify.heapify(expr, name)

    if expr in A(astlib.Name):
        #result = get(expr)
        #if result["type"] in A(astlib.CType):
        return heapify.heapify(expr, name)

    return expr, []


class Copying(layers.Layer):

    def body(self, body):
        reg = Copying().get_registry()
        return list(itertools.chain.from_iterable(
            map(lambda stmt: list(
                    layers.transform_node(stmt, registry=reg)),
                body)))

    @layers.register(astlib.VarDecl)
    def var_decl(self, declaration):
        new_expr, assignments = e(
            declaration.expr, declaration.name)
        add_to_env(declaration)
        yield astlib.VarDecl(
            declaration.name, declaration.type_,
            new_expr)
        yield from assignments

    @layers.register(astlib.LetDecl)
    def let_decl(self, declaration):
        new_expr, assignments = e(
            declaration.expr, declaration.name)
        add_to_env(declaration)
        yield astlib.LetDecl(
            declaration.name, declaration.type_,
            new_expr)
        yield from assignments

    @layers.register(astlib.AssignmentAndAlloc)
    def assignment_and_alloc(self, stmt):
        new_expr, assignments = e(stmt.expr, stmt.name)
        yield astlib.Assignment(stmt.name, "=", new_expr)
        yield from assignments

    @layers.register(astlib.Assignment)
    def assignment(self, stmt):
        expr_type = inference.infer(stmt.expr)
        if expr_type in A(astlib.Name):
            yield from self.assignment_and_alloc(
                astlib.AssignmentAndAlloc(
                    stmt.variable, expr_type, stmt.expr))
        else:
            yield heapify.get_assignment(stmt.variable, stmt.expr)

    @layers.register(astlib.Return)
    def return_(self, return_):
        # We don't use e function, for now.
        yield return_

    @layers.register(astlib.FuncDecl)
    def func(self, declaration):
        add_to_env(declaration)
        add_scope()
        yield astlib.FuncDecl(
            declaration.name, declaration.args,
            declaration.rettype, self.body(declaration.body))
        del_scope()

    @layers.register(astlib.StructFuncDecl)
    def struct_func_decl(self, declaration):
        add_to_env(declaration)
        add_scope()
        yield astlib.StructFuncDecl(
            declaration.struct, declaration.func,
            declaration.args, declaration.rettype,
            self.body(declaration.body))
        del_scope()

    @layers.register(astlib.StructDecl)
    def struct(self, declaration):
        add_to_env(declaration)
        add_scope()
        yield astlib.StructDecl(
            declaration.name, declaration.var_types,
            self.body(declaration.body))
        del_scope()
