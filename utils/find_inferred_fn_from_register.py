
def find_inferred_fn_from_register(node: nodes.NodeNG) -> nodes.FunctionDef | None:
    # func.register are function calls or register attributes
    # when the function is annotated with types
    match node:
        case nodes.Call(func=func) | (nodes.Attribute() as func):
            pass
        case _:
            return None

    if not (isinstance(func, nodes.Attribute) and func.attrname == "register"):
        return None

    func_def = safe_infer(func.expr)
    if not isinstance(func_def, nodes.FunctionDef):
        return None

    return func_def

