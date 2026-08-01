
def _get_placeholder_expr(sym_node: SymNode) -> sympy.Expr:
    shape_env = sym_node.shape_env
    if shape_env is None:
        raise AssertionError("shape_env is required for _get_placeholder_expr")
    result = sym_node._expr
    if result in shape_env.unbacked_renamings:
        return shape_env.unbacked_renamings[result]
    return result

