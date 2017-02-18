"""Parse input and return low-level AST."""

import sys

from vendor.ply import lex
from vendor.ply import yacc

from . import ast
from . import defs
from . import errors
from . import lexer_defs


# Import tokens from lexer_defs.
tokens = lexer_defs.tokens

# Precedence of operators. Last operators have higher precedence.
precedence = (
    ("right", "LE", "GE", "LT", "GT"),
    ("right", "EQ", "NE"),
    ("right", "PLUS", "MINUS"),
    ("right", "TIMES", "DIVIDE"),
)


def add_to_list(dest, src):
    """Append an item to list (if item is a list, flatten)."""
    if isinstance(src, list):
        dest.extend(src)
    else:
        dest.append(src)


def list_parsed_content(content):
    """Move parsed content (without punctuation) into a list."""
    content[0] = []
    for tok in content[1:]:
        if tok not in (",", "."):
            add_to_list(content[0], tok)
    return content[0]


def list_expr(expression):
    """Move parsed expression into a list in polish notation."""
    if len(expression) == 3 + 1:
        return [expression[2], expression[1], expression[3]]
    return [expression[1]]


# AST.
def p_ast_1(content):
    """ast : ast pair"""
    content[0] = list_parsed_content(content)


def p_ast_2(content):
    """ast : pair"""
    content[0] = [content[1]]  # AST must be list.


# Pair.
def p_pair(content):
    """pair : stmt"""
    content[0] = ast.Pair(line=content.lineno(0), stmt=content[1])


# Statement.
def p_stmt(content):
    """
    stmt : assignment_stmt
    """
    # Atom_expr can be a func call.
    # atom_expr -> atom trailers
    # func_call -> VARIABLE_NAME (args)
    content[0] = content[1]


# Assignment statement.
def p_assignment_stmt_1(content):
    """assignment_stmt : VAR VARIABLE_NAME COLON type assignop expr"""
    content[0] = ast.Assignment(
        name=content[2], type_=content[4], value=content[6])


def p_assignment_stmt_2(content):
    """assignment_stmt : VAR VARIABLE_NAME COLON type"""
    content[0] = ast.Assignment(
        name=content[2], type_=content[4], value=None)


def p_assignment_stmt_3(content):
    """assignment_stmt : VARIABLE_NAME assignop bool_expr"""
    content[0] = ast.Assignment(
        name=content[1], type_=ast.UnknownType, value=content[3])


def p_assignment_stmt_4(content):
    """assignment_stmt : VAR VARIABLE_NAME assignop bool_expr"""
    content[0] = ast.Assignment(
        name=content[2], type_=ast.UnknownType, value=content[4])


# Type.
def p_type(content):
    """
    type : TYPE_INTEGER
         | TYPE_STRING
         | TYPE_NAME
    """
    content[0] = content[1]


# Assignment operator.
def p_assignop(content):
    """assignop : EQUAL"""
    content[0] = content[1]


# Bool operator.
def p_boolop(content):
    """
    boolop : EQ
           | NE
           | LE
           | GE
           | LT
           | GT
    """
    content[0] = content[1]


# Bool expression.
def p_bool_expr_1(content):
    """bool_expr : bool_expr boolop expr"""
    content[0] = list_expr(content)


def p_bool_expr_2(content):
    """bool_expr : expr"""
    content[0] = content[1]


# Expression.
def p_expr_1(content):
    """
    expr : expr PLUS expr
         | expr MINUS expr
         | expr TIMES expr
         | expr DIVIDE expr
    """
    content[0] = list_expr(content)


def p_expr_2(content):
    """expr : factor"""
    content[0] = content[1]


# Factor.
def p_factor(content):
    """factor : atom_expr"""
    content[0] = content[1]


def p_atom_expr(content):
    """atom_expr : atom"""
    content[0] = content[1]


# Atom.
def p_atom_1(content):
    """
    atom : INTEGER
         | STRING
    """
    content[0] = content[1]


def p_atom_2(content):
    """atom : LP bool_expr RP"""
    content[0] = content[2]


def p_atom_3(content):
    """atom : VARIABLE_NAME"""
    content[0] = ast.VariableName(content[1], type_=ast.UnknownType)


def p_error(content):
    """Error handling function."""
    errors.syntax_error(line=content.lineno)


def main(code):
    """Build lexer and build parser."""
    lexer = lex.lex(module=lexer_defs)
    lexer.input(code)
    parser = yacc.yacc(module=sys.modules[__name__], debug=False)
    # Parse data got from lexer.
    ast_ = parser.parse(input=code, lexer=lexer, tracking=True)
    return ast_
