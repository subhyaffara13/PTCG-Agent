
def check_ast_node(name):
    "Check if the given name is that of a valid AST node."
    try:
        # These ast Node types were deprecated in Python 3.12 and removed
        # in Python 3.14, but plugins may still check on them.
        if sys.version_info >= (3, 12) and name in (
            "Num",
            "Str",
            "Ellipsis",
            "NameConstant",
            "Bytes",
        ):
            return name

        node = getattr(ast, name)
        if issubclass(node, ast.AST):
            return name
    except AttributeError:  # nosec(tkelsey): catching expected exception
        pass

    raise TypeError(f"Error: {name} is not a valid node type in AST")

