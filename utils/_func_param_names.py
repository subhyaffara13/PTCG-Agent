
def _func_param_names(node):
    """Get parameter names from a FunctionDef node."""
    names = set()
    names.update(a.arg for a in node.args.args)
    names.update(a.arg for a in node.args.kwonlyargs)
    if node.args.vararg: names.add(node.args.vararg.arg)
    if node.args.kwarg: names.add(node.args.kwarg.arg)
    return names

