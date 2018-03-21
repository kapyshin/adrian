from collections import OrderedDict

from . import layers, astlib, errors, defs
from .context import context
from .utils import A, split_body, only_fields


SELF = astlib.Name("self")


def totype(struct_decl):
    params = struct_decl.params
    if params:
        return astlib.ParamedType(struct_decl.name, params)
    return struct_decl.name


def field_maker(struct_name):
    def wrapper(field_name):
        return astlib.DataMember(
            astlib.DataT.struct, struct_name, field_name)
    return wrapper

self_field = field_maker(SELF)


def copy(type_, name):
    return astlib.Callable(
        astlib.CallableT.struct_func,
        type_, defs.COPY_METHOD, [name])

def malloc(name):
    return astlib.Callable(
        astlib.CallableT.cfunc, astlib.Empty(), astlib.Name("malloc"),
        [astlib.Callable(
            astlib.CallableT.cfunc, astlib.Empty(), astlib.Name("sizeof"),
            [astlib.StructScalar(name)])])


def free(name):
    return astlib.Callable(
        astlib.CallableT.cfunc, astlib.Empty(),
        astlib.Name("free"), [name])


def deinit(struct, name):
    return astlib.Callable(
        astlib.CallableT.struct_func, struct,
        astlib.Name(defs.DEINIT_METHOD), [name])


def mtostructf(method, struct):
    args = method.args
    body = method.body
    return astlib.CallableDecl(
        astlib.DeclT.struct_func, struct.name,
        method.name, args, method.rettype, body)


def ptoprotocolf(pfunc, protocol):
    args = pfunc.args
    body = pfunc.body
    return astlib.CallableDecl(
        astlib.DeclT.protocol_func, protocol.name,
        pfunc.name, args, pfunc.rettype, body)


class ObjectProtocol(layers.Layer):

    def complete_init_method(self, method, stmt):
        errors.not_now(errors.CUSTOM_OBJMETHOD)

    def complete_deinit_method(self, method, stmt):
        errors.not_now(errors.CUSTOM_OBJMETHOD)

    def complete_copy_method(self, method, stmt):
        errors.not_now(errors.CUSTOM_OBJMETHOD)

    def default_deinit_method(self, stmt):
        body = [deinit(
            field_decl.type_, self_field(field_decl.name))
            for field_decl in only_fields(stmt.body)] + [free(SELF)]
        return astlib.CallableDecl(
            astlib.DeclT.method, astlib.Empty(),
            astlib.Name(defs.DEINIT_METHOD),
            [astlib.Arg(SELF, totype(stmt))],
            astlib.Name("Void"), body)

    def default_copy_method(self, stmt):
        new = astlib.Name("new")
        field_of_new = field_maker(new)
        new_decl = astlib.Decl(
            astlib.DeclT.var, new, totype(stmt), malloc(stmt.name))
        field_inits = []
        for field_decl in only_fields(stmt.body):
            field_inits.append(astlib.Assignment(
                field_of_new(field_decl.name), "=",
                copy(field_decl.type_,
                    self_field(field_decl.name))))
        return_new = astlib.Return(new)
        body = [new_decl] + field_inits + [return_new]
        return astlib.CallableDecl(
            astlib.DeclT.method, astlib.Empty(),
            astlib.Name(defs.COPY_METHOD),
            [astlib.Arg(SELF, totype(stmt))],
            totype(stmt), body)

    def default_init_method(self, stmt):
        self_decl = astlib.Decl(
            astlib.DeclT.var, SELF, totype(stmt), malloc(stmt.name))
        return_self = astlib.Return(SELF)
        field_inits, args = [], []
        for field_decl in only_fields(stmt.body):
            args.append(astlib.Arg(field_decl.name, field_decl.type_))
            field_inits.append(
                astlib.Assignment(
                    self_field(field_decl.name), "=",
                    copy(field_decl.type_, field_decl.name)))
        body = [self_decl] + field_inits + [return_self]
        rettype = totype(stmt)
        return astlib.CallableDecl(
            astlib.DeclT.method, astlib.Empty(),
            astlib.Name(defs.INIT_METHOD),
            args, rettype, body)

    def method(self, method, struct):
        args = method.args
        body = method.body
        return astlib.CallableDecl(
            astlib.DeclT.method, astlib.Empty(), method.name,
            [astlib.Arg(SELF, totype(struct))] + args,
            method.rettype, body)

    @layers.register(astlib.DataDecl)
    def data_decl(self, stmt):
        if stmt.decltype == astlib.DeclT.struct:
            fields, methods = split_body(stmt.body)
            have = OrderedDict(sorted({
                key: (
                    i, False,
                    getattr(self, "_".join(["complete", mname])),
                    getattr(self, "_".join(["default", mname])))
                for i, key, mname in (
                    (1, defs.INIT_METHOD, "init_method"),
                    (2, defs.COPY_METHOD, "copy_method"),
                    (3, defs.DEINIT_METHOD, "deinit_method"),
                )
            }.items(), key=lambda x: x[1]))
            new_methods = []
            for method in methods:
                entry = have.get(str(method.name))
                if entry:
                    have.update({str(method.name): (True, entry[1], entry[2])})
                    new_methods.append(entry[1](method, stmt))
                else:
                    new_methods.append(self.method(method, stmt))
            additional_methods = []
            for method_name, (_, exists, _, f) in have.items():
                if not exists:
                    additional_methods.append(f(stmt))
            yield astlib.DataDecl(
                stmt.decltype, stmt.name,
                stmt.params, fields + [
                    mtostructf(method, stmt)
                    for method in additional_methods + new_methods])
        elif stmt.decltype == astlib.DeclT.protocol:
            fields, pfuncs = split_body(stmt.body)
            yield astlib.DataDecl(
                stmt.decltype, stmt.name, stmt.params,
                fields + [
                    ptoprotocolf(pfunc, stmt) for pfunc in pfuncs])
        else:
            yield astlib.DataDecl(
                stmt.decltype, stmt.name, stmt.params, stmt.body)
