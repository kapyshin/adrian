from .context import context
from . import astlib


class A:

    def __init__(self, *types):
        self.types = types

    def __contains__(self, other):
        return isinstance(other, self.types)


def _is_node_type(*nodet):
    def wrapper(name):
        return context.env[name]["node_type"] in nodet
    return wrapper

is_struct = _is_node_type(astlib.NodeT.struct)
is_var = _is_node_type(astlib.NodeT.var)
is_let = _is_node_type(astlib.NodeT.let)
is_fun = _is_node_type(astlib.NodeT.fun)
is_protocol = _is_node_type(astlib.NodeT.protocol)
is_adt = _is_node_type(astlib.NodeT.adt)
is_type = _is_node_type(
    astlib.NodeT.struct, astlib.NodeT.commont,
    astlib.NodeT.adt, astlib.NodeT.protocol)

def split_body(body):
    fields, methods = [], []
    if body in A(astlib.Empty):
        return [], []
    for stmt in body:
        if (stmt in A(astlib.Decl) and
                stmt.decltype == astlib.DeclT.field):
            fields.append(stmt)
        else:
            methods.append(stmt)
    return fields, methods


def only_fields(body):
    return split_body(body)[0]


def declt_to_nodet(declt):
    nodet = astlib.NodeT.adt
    if declt == astlib.DeclT.struct:
        nodet = astlib.NodeT.struct
    elif declt == astlib.DeclT.protocol:
        nodet = astlib.NodeT.protocol
    elif declt == astlib.DeclT.var:
        nodet = astlib.NodeT.var
    elif declt == astlib.DeclT.let:
        nodet = astlib.NodeT.let
    return nodet


def add_dicts(dict1, dict2):
    dict_ = dict1
    for key, value in dict2.items():
        dict_[key] = value
    return dict_
