import hashlib

from . import lex_parse
from . import naming_rules
from . import name_existence
from . import type_inference
from . import type_checking
from . import default_value
# from . import name_mangling
from . import ast as margo_ast


def _get_file_hash(file_name):
    obj = hashlib.sha1()
    with open(file_name, mode="rb") as file:
        obj.update(file.read())
    return obj.hexdigest()


def _read_file(file_name, encoding):
    with open(file_name, mode="r", encoding=encoding) as file:
        contents = file.read()
    return contents.splitlines()


def compile(text, context, mangle_names=False, file_hash=""):
    print("Stage 1: parsing code.")
    lp_ast = lex_parse.main(text, exit_on_error=context.exit_on_error)
    print("Stage 2: checking naming rules.")
    naming_rules.main(lp_ast, context=context)
    print("Stage 3: checking name existence.")
    name_existence.main(lp_ast, context=context)
    print("Stage 4: doing type inference where needed.")
    ti_ast = type_inference.main(lp_ast, context=context)
    print("Stage 5: checking types.")
    type_checking.main(ti_ast, context=context)
    print("Stage 6: adding default values where needed.")
    dv_ast = default_value.main(ti_ast, context=context)
    print("Compiled.")
    return dv_ast


def compile_file(file_name, exit_on_error=True, mangle_names=False, encoding="utf-8"):
    return "\n".join([
        compile(
            line, exit_on_error=exit_on_error,
            mangle_names=mangle_names, file_hash=_get_file_hash(file_name))
        for line in _read_file(file_name, encoding)
    ])
