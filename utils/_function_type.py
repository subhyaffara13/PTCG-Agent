
def _function_type(
    function: nodes.Lambda | nodes.FunctionDef | bases.UnboundMethod,
    builtins: nodes.Module,
) -> nodes.ClassDef:
    if isinstance(function, (scoped_nodes.Lambda, scoped_nodes.FunctionDef)):
        if function.root().name == "builtins":
            cls_name = "builtin_function_or_method"
        else:
            cls_name = "function"
    elif isinstance(function, bases.BoundMethod):
        cls_name = "method"
    else:
        cls_name = "function"
    return _build_proxy_class(cls_name, builtins)

