
def _advise_is_bounded(a: SymInt, upper_bound: IntLikeType) -> None:
    if (
        isinstance(a, SymInt)
        and isinstance(a.node, SymNode)
        and isinstance(a.node.expr, sympy.Symbol)
        and a.node.shape_env is not None
        and a.node.shape_env.is_unbacked_symint(a.node.expr)
        and isinstance(upper_bound, int)  # TODO: relax
    ):
        a.node.shape_env._constrain_is_bounded(a.node.expr, upper_bound)

