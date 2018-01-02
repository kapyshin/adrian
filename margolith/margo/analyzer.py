"""
Translates some FuncCalls to StructCall and StructFuncCall objects.
Infer types.
"""

import os

from . import layers, astlib, errors, defs, inference
from .context import (
    context, add_to_env, add_scope, del_scope,
    get_node_type, NodeType)
from .patterns import A


def unsupported_module():
    errors.not_implemented("only c module is supported")


def is_user_type(name):
    return get_node_type(name) == NodeType.struct


def find_cmodule(module_name):
    for directory in context.libs:
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)) and file == module_name + ".c":
                return os.path.join(directory, file)
    errors.cant_find_module(module_name)


class Analyzer(layers.Layer):

    def check_body(self, body, string):
        if body == []:
            errors.not_implemented(
                "empty {} are not supported".format(string))

    def infer_type(self, type_, expr):
        if type_ in A(astlib.Unknown):
            return inference.infer(expr)
        return type_

    def call_args(self, args):
        return list(map(self.e, args))

    def decl_args(self, args):
        return [astlib.Arg(arg.name, self.t(arg.type_)) for arg in args]

    def type_parameters(self, types):
        return list(map(self.t, types))

    def e_func_call(self, stmt):
        if stmt.name in A(astlib.ModuleMember):
            if stmt.name.module != defs.CMODULE_NAME:
                unsupported_module()
            context.clibs.append(find_cmodule("adrian_" + defs.CMODULE_NAME))
            yield astlib.StructCall(
                stmt.name, [astlib.IntLiteral(stmt.args[0].literal)])
            # yield getattr(
            #     astlib, "C" + str(stmt.name.member))(stmt.args[0].literal)
        elif str(stmt.name) == defs.REF:
            yield astlib.Ref(self.call_args(stmt.args)[0])
        elif is_user_type(stmt.name):
            yield astlib.StructCall(
                stmt.name, self.call_args(stmt.args))
        else:
            yield astlib.FuncCall(
                stmt.name, self.call_args(stmt.args))

    def e_struct_member(self, stmt):
        if stmt.member in A(astlib.FuncCall):
            func_call = stmt.member
            analyzed_struct = self.e(stmt.struct)
            return astlib.StructFuncCall(
                struct=inference.infer(analyzed_struct),
                func_name=func_call.name,
                args=[analyzed_struct] + self.call_args(func_call.args))
        if stmt.member in A(astlib.Name):
            return astlib.StructMember(
                struct=self.e(stmt.struct),
                member=stmt.member)

    def e(self, expr):
        if expr in A(astlib.FuncCall):
            return list(self.e_func_call(expr))[0]
        if expr in A(astlib.StructMember):
            return self.e_struct_member(expr)
        if expr in A(astlib.Expr):
            return astlib.Expr(
                expr.op,
                self.e(expr.left_expr),
                self.e(expr.right_expr))
        return expr

    def t(self, type_):
        if type_ in A(astlib.ModuleMember):
            if type_.module == defs.CMODULE_NAME:
                return type_
            unsupported_module()
        if type_ in A(astlib.Name):
            if type_ == "Void":
                return astlib.CVoid()
        if type_ in A(astlib.ParameterizedType):
            return astlib.ParameterizedType(
                type_.type_, self.type_parameters(type_.parameters))
        return type_

    def body(self, body):
        reg = Analyzer().get_registry()
        return list(map(
            lambda stmt: list(
                layers.transform_node(stmt, registry=reg))[0], body))

    def _decl(self, stmt):
        expr = self.e(stmt.expr)
        type_ = self.t(self.infer_type(stmt.type_, expr))
        result = type(stmt)(stmt.name, type_, expr)
        add_to_env(result)
        yield result

    @layers.register(astlib.VarDecl)
    def decl(self, stmt):
        yield from self._decl(stmt)

    @layers.register(astlib.LetDecl)
    def ldecl(self, stmt):
        yield from self._decl(stmt)

    @layers.register(astlib.Assignment)
    def assignment(self, stmt):
        yield astlib.Assignment(
            self.e(stmt.variable), stmt.op, self.e(stmt.expr))

    @layers.register(astlib.AssignmentAndAlloc)
    def assignment_and_alloc(self, stmt):
        yield astlib.AssignmentAndAlloc(
            self.e(stmt.name), self.t(stmt.type_), self.e(stmt.expr))

    @layers.register(astlib.Return)
    def return_(self, stmt):
        yield astlib.Return(self.e(stmt.expr))

    @layers.register(astlib.FuncDecl)
    def func_decl(self, stmt):
        self.check_body(stmt.body, "functions")
        add_to_env(stmt)
        add_scope()
        body = self.body(stmt.body)
        yield astlib.FuncDecl(
            stmt.name, self.decl_args(stmt.args),
            self.t(stmt.rettype), body)
        del_scope()

    @layers.register(astlib.StructFuncDecl)
    def method_decl(self, stmt):
        self.check_body(stmt.body, "methods")
        add_to_env(stmt)
        add_scope()
        body = self.body(stmt.body)
        yield astlib.StructFuncDecl(
            stmt.struct, stmt.func, self.decl_args(stmt.args),
            self.t(stmt.rettype), body)
        del_scope()

    @layers.register(astlib.FieldDecl)
    def field_decl(self, stmt):
        yield astlib.FieldDecl(
            stmt.name, self.t(stmt.type_))

    @layers.register(astlib.FuncCall)
    def func_call(self, stmt):
        yield from self.e_func_call(stmt)

    @layers.register(astlib.StructMember)
    def struct_member(self, stmt):
        yield self.e_struct_member(stmt)

    @layers.register(astlib.StructDecl)
    def struct_decl(self, stmt):
        self.check_body(stmt.body, "structures")
        add_to_env(stmt)
        add_scope()
        body = self.body(stmt.body)
        yield astlib.StructDecl(
            stmt.name, stmt.var_types, body)
        del_scope()
