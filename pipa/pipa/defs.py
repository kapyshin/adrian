import re
import copy
from functools import partial

from . import astlib, env


MANGLING_LENGTH = 6


MODULE_PRELUDE = "prelude"
TYPE_NUMBER = "Number"
TYPE_STRING = "String"
TYPE_BOOL = "Bool"
TYPE_VECTOR = "Vector"
TYPE_SET = "Set"
TYPE_DICT = "Dict"
TYPE_SOME = "Some"
TYPE_NONE = "None"
TYPE_MAYBE = "Maybe"
PRELUDE_TYPES = (
    TYPE_NUMBER, TYPE_STRING, TYPE_BOOL, TYPE_VECTOR,
    TYPE_SET, TYPE_DICT, TYPE_SOME, TYPE_NONE, TYPE_MAYBE)
FUNC_PRINT = "print"
FUNC_LENGTH = "length"
PRELUDE_FUNCS = (FUNC_PRINT, FUNC_LENGTH)


MODULE_PY = "py"
TYPE_INT = "Int"
TYPE_STR = "Str"
TYPE_LIST = "List"
FUNC_TO_INT = "toInt"
FUNC_TO_STR = "toStr"
FUNC_TO_SET = "toSet"
FUNC_TO_LIST = "toList"
FUNC_LEN = "len"
FUNC_READ_FILE = "readFile"
FUNC_WRITE_FILE = "writeFile"
METHOD_SPLIT = "split"
METHOD_VALUES = "values"
METHOD_KEYS = "keys"
METHOD_ITEMS = "items"


RESERVED_WORDS = {
    keyword: keyword.upper()
    for keyword in (
        "var", "let", "for", "in"
    )
}

NAME_REGEX = re.compile(r"[a-z][a-zA-Z0-9]*")
FUNC_REGEX = NAME_REGEX
TYPE_REGEX = re.compile(r"[A-Z][a-zA-Z0-9]*")
MODULE_REGEX = re.compile(r"[a-z][a-z_0-9]*")
METHOD_REGEX = re.compile(
    r"((__)[a-z][a-zA-Z0-9]*(__))|([a-z][a-zA-Z0-9]*)")
COMMON_REGEX = "".join([
    "(",
    ")|(".join([regex.pattern
        for regex in (NAME_REGEX, FUNC_REGEX,
        TYPE_REGEX, MODULE_REGEX, METHOD_REGEX)]),
    ")"])


SPEC_METHOD_ADD = "__add__"
SPEC_METHOD_SUB = "__sub__"
SPEC_METHOD_MUL = "__mul__"
SPEC_METHOD_DIV = "__div__"
OPERATOR_TO_METHOD = {
    "+": SPEC_METHOD_ADD,
    "-": SPEC_METHOD_SUB,
    "*": SPEC_METHOD_MUL,
    "/": SPEC_METHOD_DIV,
}


ENV = env.Env()
DEFAULT_MODULE_PATHS = ["library/"]
DEFAULT_CONTEXT_ARGUMENTS = {
    "env": copy.deepcopy(ENV),
    "exit_on_error": False,
}
