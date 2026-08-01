
def size_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    """
    The constraint is just lhs = rhs.
    Ex: size = input_ids.size()
    """

    if len(n.args) == 1:
        # generate the new variable
        size, counter = gen_tvar(counter)
        symbols[n] = size
        input = symbols[n.args[0]]  # pyrefly: ignore[bad-index]
        c = BinConstraintT(input, size, op_eq)
        return [c], counter

    elif len(n.args) == 2:
        # TODO: review this rule; should input = dyn; output = dyn be included here?
        if isinstance(n.args[1], int):
            # generate the new variable
            size_index, counter = gen_dvar(counter)
            symbols[n] = size_index
            input = symbols[n.args[0]]  # pyrefly: ignore[bad-index]
            c2 = [
                GetItem(
                    i + 1,
                    n.args[1],
                    size_index,
                    input,  # pyrefly: ignore[bad-argument-type]
                )
                for i in range(MAX_TENSOR_RANK)
            ]
            c3 = BinConstraintD(0, size_index, op_leq)

            input_dyn = BinConstraintT(input, Dyn, op_eq)
            output_dyn = BinConstraintD(size_index, Dyn, op_eq)
            c1 = Conj([input_dyn, output_dyn])

            return [Disj([c1, Conj([Disj(c2), c3])])], counter

        else:
            raise NotImplementedError

    else:
        raise NotImplementedError

