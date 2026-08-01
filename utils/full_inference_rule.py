
def full_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    full, counter = gen_tvar(counter)
    symbols[n] = full
    res = []

    if not isinstance(n.args[0], Iterable):
        raise AssertionError(f"Expected Iterable, got {type(n.args[0])}")
    for arg in n.args[0]:
        dim = (
            arg if isinstance(arg, int) else symbols[arg]  # pyrefly: ignore[bad-index]
        )
        res.append(dim)
    c = BinConstraintT(full, TensorType(list(res)), op_eq)  # type: ignore[arg-type]
    return [c], counter

