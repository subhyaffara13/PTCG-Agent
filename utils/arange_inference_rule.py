
def arange_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    start = 0
    step = 1

    if len(n.args) == 1:
        end = symbols[n.args[0]]  # pyrefly: ignore[bad-index]
    else:
        raise NotImplementedError("Not yet implemented")

    # int((end - start) / step)
    d1, counter = gen_dvar(counter)
    size_constraint = BinConstraintD(
        d1, BinConstraintD(BinConstraintD(end, start, op_sub), step, op_div), op_eq
    )
    arange, counter = gen_tvar(counter)
    symbols[n] = arange

    # either the a parameter is a number or it is Dyn
    c1 = Disj(
        [
            BinConstraintD(end, Dyn, op_eq),
            BinConstraintD(start, Dyn, op_eq),
            BinConstraintD(step, Dyn, op_eq),
        ]
    )
    c2 = BinConstraintD(d1, Dyn, op_eq)
    both_dyn = Conj([c1, c2])

    c11 = Conj(
        [
            BinConstraintD(end, Dyn, op_neq),
            BinConstraintD(start, Dyn, op_neq),
            BinConstraintD(step, Dyn, op_neq),
        ]
    )
    c22 = BinConstraintD(d1, Dyn, op_neq)
    both_numbers = Conj([c11, c22, size_constraint])

    return [
        BinConstraintT(arange, TensorType([d1]), op_eq),
        Disj([both_dyn, both_numbers]),
    ], counter

