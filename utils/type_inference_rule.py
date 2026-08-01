
def type_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    """
    We generate the constraint: input = output
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    if not isinstance(n.args[1], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[1])}")

    output, counter = gen_tvar(counter)
    symbols[n] = output

    from_arg = symbols[n.args[0]]
    to_arg = symbols[n.args[1]]

    if not isinstance(from_arg, TVar):
        raise AssertionError(f"Expected TVar, got {type(from_arg)}")
    if not isinstance(to_arg, TVar):
        raise AssertionError(f"Expected TVar, got {type(to_arg)}")

    return [
        BinConstraintT(from_arg, to_arg, op_consistency),
        BinConstraintT(output, to_arg, op_eq),
    ], counter

