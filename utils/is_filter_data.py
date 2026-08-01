
def is_filter_data(context):
    for keyword in context.node.keywords:
        if keyword.arg == "filter":
            arg = keyword.value
            return isinstance(arg, ast.Constant) and arg.value == "data"

