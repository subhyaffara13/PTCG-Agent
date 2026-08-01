
def get_called_name(node):
    """Get a function name from an ast.Call node.

    An ast.Call node representing a method call with present differently to one
    wrapping a function call: thing.call() vs call(). This helper will grab the
    unqualified call name correctly in either case.

    :param node: (ast.Call) the call node
    :returns: (String) the function name
    """
    func = node.func
    try:
        return func.attr if isinstance(func, ast.Attribute) else func.id
    except AttributeError:
        return ""

