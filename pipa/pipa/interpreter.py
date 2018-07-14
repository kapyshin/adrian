from . import astlib, layers, errors, defs
from .context import context
from .utils import A


class Interpreter(layers.Layer):

    def adr_to_py(self, expr):
        if expr in A(astlib.FuncCall):
            return self.func_call(expr)
        elif expr in A(astlib.Name):
            return self.adr_to_py(context.env[expr]["expr"])
        else:
            # support other exprs
            errors.later()

    @layers.register(astlib.LetDecl)
    def let_declaration(self, declaration):
        context.env[declaration.name] = {
            "node_type": astlib.NodeT.let,
            "type": declaration.type_,
            "expr": declaration.expr
        }

    @layers.register(astlib.FuncCall)
    def func_call(self, func_call):
        if func_call.name in A(astlib.ModuleMember):
            if func_call.name.module == defs.MODULE_PY:
                return self.py_func_call(
                    astlib.FuncCall(func_call.name.member, func_call.args))
            else:
                # support other modules
                errors.later()
        else:
            # support defined functions
            errors.later()

    def py_func_call(self, func_call):
        if func_call.name == defs.TYPE_INT:
            return int(func_call.args[0].literal)
        elif func_call.name == defs.TYPE_STR:
            return func_call.args[0].literal
        elif func_call.name == defs.FUNC_PRINT:
            for arg in func_call.args:
                print(self.adr_to_py(arg))
        else:
            # support other funcs
            errors.later()
