import copy

from adrian import cgen as adr_cgen

from . import parser, foreign_parser, analyzer
from . import name_existence_checking, types_phase, object_proto
from . import tac, copying, arc, name_spacing
from . import method_to_func, tocgen, main_func
from . import env, context, layers


REPL_FILE_HASH = "mangled"

LAYERS = (
    (parser.Parser, "parse"),
    (analyzer.Analyzer, "transform_ast"),
    (name_existence_checking.NameExistence, "transform_ast"),
    (types_phase.TypeInference, "transform_ast"),
    (object_proto.ObjectProto, "transform_ast"),
    (tac.TAC, "transform_ast"),
    (copying.Copying, "transform_ast"),
    (arc.ARC, "expand_ast"),
    (method_to_func.MethodToFunc, "transform_ast"),
    (name_spacing.NameSpacing, "transform_ast"),
    (tocgen.ToCGen, "transform_ast"),
    (main_func.MainFunc, "expand_ast")
)


def compile_repl(inp, *, contexts):
    for layer_cls, method_name in LAYERS:
        with context.new_context(**copy.deepcopy(contexts[layer_cls])):
            layer = layer_cls()
            if not method_name == "parse":
                current_ast = list(getattr(layers, method_name)(
                    current_ast, registry=layer.get_registry()))
            else:
                current_ast = foreign_parser.main(
                    layer.parse(inp))
    generator = adr_cgen.Generator()
    generator.add_ast(current_ast)
    return "\n".join(generator.generate())
    # return current_ast


def compile_from_string(inp, file_hash):
    contexts = {
        layer: {
            "env": env.Env(),
            "exit_on_error": True,
            "file_hash": file_hash,
            "tmp_count": 0}
        for layer, _ in LAYERS
    }
    for layer_cls, method_name in LAYERS:
        with context.new_context(**contexts[layer_cls]):
            layer = layer_cls()
            if not method_name == "parse":
                current_ast = list(getattr(layers, method_name)(
                    current_ast, registry=layer.get_registry()))
            else:
                current_ast = foreign_parser.main(
                    layer.parse(inp))
            contexts[layer_cls]["tmp_count"] = context.context.tmp_count
    generator = adr_cgen.Generator()
    generator.add_ast(current_ast)
    return "\n".join(generator.generate())


def _read_file(file_name, encoding):
    with open(file_name, mode="r", encoding=encoding) as file:
        contents = file.read()
    return contents


def compile_from_file(in_file, file_hash):
    return compile_from_string(
        _read_file(in_file, "utf-8"), file_hash=file_hash)
