
def param_names(node):
    names = set()
    names.update(a.arg for a in node.args.args)
    names.update(a.arg for a in node.args.kwonlyargs)
    if node.args.vararg:
        names.add(node.args.vararg.arg)
    if node.args.kwarg:
        names.add(node.args.kwarg.arg)
    return names

