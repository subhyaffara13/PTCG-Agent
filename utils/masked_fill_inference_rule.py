
def masked_fill_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    """
    Similar to addition. For now we implement the constraints when
    the argument is a boolean tensor. There is also a case for when
    it is a condition. We will leave this out for now.
    """

    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    if not isinstance(n.args[1], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[1])}")

    # We will retrieve the type variables from the symbol table
    # and confirm they are tensor variables

    e1 = symbols[n.args[0]]
    e2 = symbols[n.args[1]]

    if isinstance(e1, TVar) and isinstance(e2, TVar):
        masked_fill_tensor, counter = gen_tvar(counter)
        symbols[n] = masked_fill_tensor
        return gen_broadcasting_constraints(
            e1, e2, symbols, counter, masked_fill_tensor
        )
    else:
        raise NotImplementedError("Not yet implemented")

