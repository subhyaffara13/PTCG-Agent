
def layer_norm_functional(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    """
    We generate the constraint: input = output
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    return gen_layer_norm_constraints(
        n,
        n.args[1],  # pyrefly: ignore[bad-argument-type]
        symbols,
        counter,
    )

