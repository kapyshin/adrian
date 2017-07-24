"""Generates CGen AST."""

from . import cdefs, layers, astlib, errors
from vendor.adrian import cgen


TO_CTYPE = {
    "IntFast8": "int_fast8",
    "IntFast32": "int_fast32",
    "UIntFast8": "uint_fast8",
    "UIntFast32": "uint_fast32",
}


class CGen(layers.Layer):

    def _type(self, type_):
        # Only c types are supported.
        if isinstance(type_, astlib.CType):
            return getattr(cgen.CTypes, TO_CTYPE[str(type_)])
        errors.not_implemented()

    def _expr(self, expr):
        if isinstance(expr, astlib.SExpr):
            return cgen.Expr(
                op=expr.op, expr1=self._expr(expr.expr1),
                expr2=self._expr(expr.expr2))
        elif isinstance(
                expr, (
                    astlib.CIntFast8, astlib.CIntFast32,
                    astlib.CUIntFast8, astlib.CUIntFast32)):
            return cgen.Val(
                literal=expr.literal,
                type_=getattr(cgen.CTypes, TO_CTYPE[str(expr.to_type())]))
        elif isinstance(expr, astlib.CFuncCall):
            # We hope that expr is right xD
            return self._cfunc_call(expr)
        errors.not_implemented()

    def _decl(self, decl):
        return cgen.Decl(
            name=str(decl.name), type_=self._type(decl.type_),
            expr=self._expr(decl.expr))

    def _body(self, body):
        return ([] if isinstance(body, astlib.Empty) else body.as_list())
        # new_body = []
        # for stmt in ([] if isinstance(body, astlib.Empty) else body.as_list()):
        #     new_body.append(self.reg[type(stmt)](self, stmt))
        # return new_body

    def _func_args(self, args):
        new_args = []
        for arg in ([] if isinstance(args, astlib.Empty) else args.as_list()):
            new_args.append(cgen.Decl(str(arg[0]), type_=self._type(arg[1])))
        return new_args

    def _call_args(self, args):
        new_args = []
        for arg in ([] if isinstance(args, astlib.Empty) else args.as_list()):
            new_args.append(self._expr(arg.arg))
        return new_args

    def _func_decl(self, func_decl):
        return cgen.Func(
            name=str(func_decl.name), rettype=self._type(func_decl.type_),
            args=self._func_args(func_decl.args),
            body=self._body(func_decl.body))

    def _struct_decl(self, struct_decl):
        return cgen.Struct(
            name=str(struct_decl.name),
            body=self._body(struct_decl.body))

    def _field_decl(self, field_decl):
        return cgen.Decl(
            name=str(field_decl.name), type_=self._type(field_decl.type_))

    def _cfunc_call(self, func_call):
        if func_call.name == cdefs.MALLOC_FUNC_NAME:
            stdlib_include = cgen.Include("stdlib.h")
            malloc_func = cgen.CFuncDescr(
                "malloc",
                rettype=cgen.CTypes.ptr(cgen.CTypes.void),
                args=(cgen.CTypes.size_t, ),
                includes=[stdlib_include])
            return malloc_func(*self._call_args(func_call.args))
        elif func_call.name == cdefs.SIZEOF_FUNC_NAME:
            return cgen.SizeOf(cgen.StructType(str(func_call.args[0].name)))
        errors.not_implemented()

    def _return_stmt(self, return_stmt):
        return cgen.Return(expr=self._expr(return_stmt.expr))

    reg = {
        astlib.Decl: _decl,
        astlib.FuncDecl: _func_decl,
        astlib.Return: _return_stmt,
        astlib.StructDecl: _struct_decl,
        astlib.FieldDecl: _field_decl,
    }

    @layers.preregister(astlib.Pair)
    def _pair(self, pair):
        yield self.reg[type(pair.stmt)](self, pair.stmt)