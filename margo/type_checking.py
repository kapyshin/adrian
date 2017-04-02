from . import ast
from . import defs
from . import errors
from . import layers

from vendor.paka import funcreg


_FUNCS = funcreg.TypeRegistry()


def str_type(value, *, context):
    if isinstance(value, defs.NAME_TYPES):
        entry = context.namespace.get(value.value)
        if entry:
            return entry["type"]
    return value.to_string()


def check_type_of_value(value, *, context):
    """Validate value (atom or a list of atoms) and return its type."""
    if isinstance(value, defs.NAME_TYPES):
        return str_type(value, context=context)
    elif isinstance(value, defs.ATOM_TYPES):
        return str_type(value, context=context)
    elif isinstance(value, list):
        return check_type_of_value.checker_reg[value[0]](
            check_type_of_value(value[1], context=context),
            check_type_of_value(value[2], context=context),
            context=context)


check_type_of_value.checker_reg = funcreg.NameRegistry()


@check_type_of_value.checker_reg.register("+")
def _check_plus(type1, type2, *, context):
    """Only Integer + Integer is supported."""
    if type1 == ast.Integer.to_string() == type2:
        return ast.Integer.to_string()
    errors.not_implemented(context.line, context.exit_on_error)


@check_type_of_value.checker_reg.register("-")
def _check_minus(type1, type2, *, context):
    """Only Integer - Integer is supported."""
    if type1 == ast.Integer.to_string() == type2:
        return ast.Integer.to_string()
    errors.not_implemented(context.line, context.exit_on_error)


@check_type_of_value.checker_reg.register("*")
def _check_multiply(type1, type2, *, context):
    """Only Integer * Integer is supported."""
    if type1 == ast.Integer.to_string() == type2:
        return ast.Integer.to_string()
    errors.not_implemented(context.line, context.exit_on_error)


@check_type_of_value.checker_reg.register("/")
def _check_divide(type1, type2, *, context):
    """Only Integer / Integer is supported.

    TODO: what type 1/2 has?
    """
    if type1 == ast.Integer.to_string() == type2:
        return ast.Integer.to_string()
    errors.not_implemented(context.line, context.exit_on_error)


@_FUNCS.register(ast.Assignment)
def assignment(pair, *, context):
    stmt = pair.stmt
    name = stmt.name
    context.line = pair.line
    type_of_value = check_type_of_value(stmt.value, context=context)
    if (name.type_ != type_of_value) and not (type_of_value is None):
        errors.type_of_name_and_type_of_value_are_not_equal(
            context.line, context.exit_on_error, name=name.value,
            type_of_name=name.type_, type_of_value=type_of_value)
    context.namespace.add_name(name.value, {
        "node_type": defs.NodeType.variable,
        "type": name.type_,
        "value": stmt.value
    })
    return ast.Pair(pair.line, ast.Assignment(name.value, name.type_, stmt.value))


def check(ast_, *, context):
    return [_FUNCS[pair.stmt](pair, context=context) for pair in ast_]


def main(ast_, *, exit_on_error=True):
    return check(ast_, context=ast.Context(exit_on_error))
