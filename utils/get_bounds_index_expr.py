
def get_bounds_index_expr(index: sympy.Expr) -> ValueRanges[Any]:
    from .virtualized import V

    # If this expression does not come from an FX node, we compute its bounds
    if (
        config.compute_all_bounds
        and (fx_node := getattr(V.interpreter, "current_node", None))
        and fx_node.target != "index_expr"
    ):
        return bound_sympy(index)
    else:
        return ValueRanges.unknown()

