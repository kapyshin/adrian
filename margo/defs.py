"""Contains many useful definitions."""

import re
import enum

from . import ast


RESERVED_WORDS = (
    "var",
#    "cst",
    "fun",
    "data",
    "ret",
#    "iff",
#    "else",
)


@enum.unique
class NodeType(enum.Enum):
    variable = 1
    constant = 2


CALLABLE_ATOMS = (
    ast.Name,
)

ATOM_TYPES = (
    ast.Integer,
    ast.String,
    ast.Name,
)

STD_FUNCS = (
    "print",
)

_STD_TYPES = (
    ast.Integer,
    ast.String
)
STD_TYPE_NAMES = set(type_.to_string() for type_ in _STD_TYPES)

TYPE_REGEX = re.compile(r"[A-Z_][a-zA-Z0-9]*")
VARIABLE_REGEX = re.compile(r"[a-z_][a-zA-Z0-9]*")
MODULE_REGEX = re.compile(r"[a-z_][a-z_0-9]*")
CONSTANT_REGEX = re.compile(r"[A-Z_][A-Z_0-9]*")
SPECIAL_STRUCT_ELEM_REGEX = re.compile(r"[_][_][a-zA-Z0-9]*[_][_]")

C_MODULE_NAME = "c"
C_INT32 = "Int32"
C_INT64 = "Int64"
C_CSTRING = "CString"
C_CHAR = "Char"
C_FUNC_SIGNATURES = {
    "initInt32": {
        "rettype": ast.ModuleMember(
            name=ast.Name(C_MODULE_NAME), member=ast.Name("Int32")),
    },
    "initCString": {
        "rettype": ast.ModuleMember(
            name=ast.Name(C_MODULE_NAME), member=ast.Name("CString")),
    }
}

STD_TYPES_MODULE_NAME = "std_types"
STD_TYPES_FUNC_SIGNATURES = {
    "initInteger": {
        "rettype": ast.ModuleMember(
            name=ast.Name(STD_TYPES_MODULE_NAME), member=ast.Name("Integer"))
    }
}
STD_MODULE_NAMES = (STD_TYPES_MODULE_NAME)
STD_MODULES_PATH = "std_modules/"
ADRIAN_FILE_EXTENSION = ".adr"