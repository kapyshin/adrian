from . import ast
from . import defs

from vendor.paka import funcreg
from vendor.adrian import cgen


_FUNCS = funcreg.TypeRegistry()


def ctype(type_):
    if type_.module_name == defs.CTYPES_MODULE_NAME:
        _d = {
            defs.CTYPES_INT32_STRING: cgen.CTypes.int32,
            defs.CTYPES_INT64_STRING: cgen.CTypes.int64,
            defs.CTYPES_CHAR_STRING: cgen.CTypes.char
        }
        return _d[type_.member.value]


def _generate_value(value, type_):
    if isinstance(value, ast.Name):
        return cgen.Var(value.value)
    elif isinstance(value, defs.ATOM_TYPES):
        # TODO: only ctypes type is supported
        return cgen.Val(value.value, ctype(type_))
    elif isinstance(value, list):
        # TODO: only ctypes type is supported
        return cgen.Expr(
            value[0],
            _generate_value(value[1], type_),
            _generate_value(value[2], type_)
        )


def generate_value(stmt):
    return generate_value.registry[stmt](stmt)


generate_value.registry = funcreg.TypeRegistry()


@generate_value.registry.register(ast.Assignment)
def _generate_assignment_value(stmt):
    return _generate_value(stmt.value, stmt.type_)


@_FUNCS.register(ast.Assignment)
def assignment(pair, *, context):
    return cgen.Decl(pair.stmt.name.value, generate_value(pair.stmt))


def generate(ast_, *, context):
    return [_FUNCS[pair.stmt](pair, context=context) for pair in ast_]


def main(ast_, *, context=ast.Context(
        exit_on_error=True, module_paths=["std_modules/"])):
    return generate(ast_, context=context)
