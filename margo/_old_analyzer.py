"""Analyzes names and translates them into more specific."""

from . import layers, astlib, errors
from .context import context


class Analyzer(layers.Layer):

    def _type(self, type_):
        # Only c module is supported, for now.
        if isinstance(type_, astlib.ModuleMember):
            return astlib.CType(str(type_.member))
        elif isinstance(type_, astlib.CType):
            return type_
        elif isinstance(type_, astlib.Empty):
            return type_
        errors.not_implemented()

    def _expr(self, expr):
        # Only c module is supported, for now.
        if (isinstance(expr, astlib.FuncCall) and \
                (isinstance(expr.name, astlib.ModuleMember))):
            module = expr.name
            # args = (
            #     [] if isinstance(expr, astlib.Empty)
            #     else expr.args.as_list())
            args = expr.args
            return getattr(astlib, "C" + str(module.member))(
                args.arg.literal)
        elif isinstance(expr, astlib.Name):
            return astlib.VariableName(str(expr))
        elif isinstance(expr, astlib.SExpr):
            return layers.create_with(
                expr, expr1=self._expr(expr.expr1),
                expr2=self._expr(expr.expr2))
        return expr

    @layers.preregister(astlib.Decl)
    def _decl(self, decl):
        # Maybe ns.add(decl.name)?
        yield layers.create_with(
            decl, name=astlib.VariableName(str(decl.name)),
            type_=self._type(decl.type_), expr=self._expr(decl.expr))

    def _func_decl_args(self, args):
        if isinstance(args, astlib.Empty):
            return astlib.Empty()
        return astlib.Args(
            astlib.VariableName(str(args.name)),
            self._type(args.type_),
            self._func_decl_args(args.rest))

    def _body_stmt(self, stmt, registry):
        # HARDCORE! FIXME!
        return layers.transform_ast(
            [stmt], registry=registry)[0]

    def _body(self, body, registry):
        if isinstance(body, astlib.Empty):
            return astlib.Empty()
        return astlib.Body(
            self._body_stmt(body.stmt, registry),
            self._body(body.rest, registry))

    @layers.preregister(astlib.FuncDecl)
    def _func_decl(self, func_decl):
        registry = Analyzer().get_registry()
        yield layers.create_with(
            func_decl, name=astlib.FunctionName(str(func_decl.name)),
            args=self._func_decl_args(func_decl.args),
            type_=self._type(func_decl.type_),
            body=self._body(func_decl.body, registry))

    @layers.preregister(astlib.MethodDecl)
    def _method_decl(self, method_decl):
        registry = Analyzer().get_registry()
        yield layers.create_with(
            method_decl, name=astlib.MethodName(str(method_decl.name)),
            args=self._func_decl_args(method_decl.args),
            type_=self._type(method_decl.type_),
            body=self._body(method_decl.body, registry))

    @layers.preregister(astlib.Return)
    def _return_stmt(self, return_stmt):
        yield layers.create_with(return_stmt, expr=self._expr(return_stmt.expr))

    @layers.preregister(astlib.StructDecl)
    def _struct_decl(self, struct_decl):
        registry = Analyzer().get_registry()
        yield layers.create_with(
            struct_decl, name=astlib.TypeName(str(struct_decl.name)),
            body=self._body(struct_decl.body, registry))

    @layers.preregister(astlib.FieldDecl)
    def _field_decl(self, field_decl):
        yield layers.create_with(
            field_decl, name=astlib.VariableName(str(field_decl.name)),
            type_=self._type(field_decl.type_))