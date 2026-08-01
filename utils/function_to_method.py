
def function_to_method(n, klass):
    if isinstance(n, FunctionDef):
        if n.type == "classmethod":
            return bases.BoundMethod(n, klass)
        if n.type == "property":
            return n
        if n.type != "staticmethod":
            return bases.UnboundMethod(n)
    return n

