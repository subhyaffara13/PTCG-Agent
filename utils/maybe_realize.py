
def maybe_realize(args: list[IRNode | None]):
    """Accepts a list of optional IRNodes and returns a list of realized IRNodes"""
    return tree_map(
        lambda x: (
            realize_inputs(x)
            if x is not None and not isinstance(x, sympy.Symbol)
            else x
        ),
        args,
    )

