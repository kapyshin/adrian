import importlib
import pathlib

from . import astlib, layers, errors, defs
from .context import context
from .utils import A


def n(name, hash_=None):
    hash_ = hash_ or context.main_file_hash
    return astlib.Name(
        "_".join([hash_[:defs.MANGLING_LENGTH], str(name)]))


def t(type_, hash_=None):
    hash_ = hash_ or context.main_file_hash
    if type_ in A(astlib.ModuleMember):
        if type_.module == defs.MODULE_PY:
            return make_py_object(type_.member)
        else:
            errors.later()
    elif type_ in A(astlib.Empty):
        return type_
    else:
        errors.later()


def e(expr, hash_=None):
    hash_ = hash_ or context.main_file_hash
    if expr in A(astlib.Name):
        return n(expr, hash_=hash_)
    elif expr in A(astlib.ModuleMember):
        if expr.module == defs.MODULE_PY:
            return make_py_object(expr.member)
        else:
            errors.later()
    elif expr in A(list):
        return [e(expr[0], hash_=hash_)] + [
            only_args(elem, hash_=hash_) for elem in expr[1:]]
    elif expr in A(astlib.FuncCall):
        name = e(expr.name, hash_=hash_)
        args = a(expr.args, hash_=hash_)
        if name in A(astlib.PyFunc):
            return astlib.PyFuncCall(name.name, args)
        elif name in A(astlib.PyType):
            return astlib.PyTypeCall(name.name, args)
        return astlib.FuncCall(name, args)
    elif expr in A(astlib.Literal):
        if expr.type_ == astlib.LiteralT.vector:
            return astlib.Literal(
                expr.type_, a(expr.literal, hash_=hash_))
        elif expr.type_ == astlib.LiteralT.set_:
            return astlib.Literal(
                expr.type_, set(a(expr.literal, hash_=hash_)))
        elif expr.type_ == astlib.LiteralT.dict_:
            return astlib.Literal(
                expr.type_, {
                    e(key, hash_=hash_): e(val, hash_=hash_)
                    for key, val in expr.literal.items()})
        return expr
    else:
        errors.later()


def a(args, hash_=None):
    hash_ = hash_ or context.main_file_hash
    return [e(arg, hash_=hash_) for arg in args]


def only_args(node, hash_=None):
    hash_ = hash_ or context.main_file_hash
    if node in A(astlib.FuncCall):
        return astlib.FuncCall(node.name, a(node.args))
    return node


def make_py_object(node):
    if node in (
            defs.FUNC_PRINT, defs.FUNC_LEN, defs.FUNC_TO_INT,
            defs.FUNC_TO_STR):
        return astlib.PyFunc(node)
    return astlib.PyType(node)


class Loader(layers.Layer):

    @layers.register(astlib.LetDecl)
    def let_declaration(self, declaration):
        yield astlib.LetDecl(
            n(declaration.name), t(declaration.type_), e(declaration.expr))

    @layers.register(astlib.FuncCall)
    def func_call(self, call):
        yield e(call)

    @layers.register(astlib.AST)
    def main(self, nodes, registry):
        translated_nodes = []
        for node in nodes:
            translated_nodes.extend(
                layers.transform_node(node, registry=registry))
        return context.loaded + translated_nodes
