
def index_select_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    """
    We constrain the second argument to a vector or Dyn.
    The output replaces the input with the shape of the vector
    at the position given by the index (first argument)
    """
    # print(n.args)
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    if not isinstance(n.args[1], int):
        raise AssertionError(f"Expected int, got {type(n.args[1])}")
    if not isinstance(n.args[2], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[2])}")

    index_select, counter = gen_tvar(counter)
    symbols[n] = index_select

    dims, counter = gen_tensor_dims(1, counter)

    # equality constraint
    is_size_1 = BinConstraintT(symbols[n.args[2]], TensorType(dims), op_eq)
    is_dyn = BinConstraintT(symbols[n.args[2]], Dyn, op_eq)

    c2 = Conj(
        [
            is_size_1,
            Disj(
                [
                    IndexSelect(
                        i + 1,
                        symbols[  # pyrefly: ignore[bad-argument-type, bad-index]
                            n.args[0]
                        ],
                        dims[0],
                        n.args[1],
                        index_select,
                    )
                    for i in range(MAX_TENSOR_RANK)
                ]
            ),
        ]
    )
    c3 = Conj(
        [
            is_dyn,
            Disj(
                [
                    IndexSelect(
                        i + 1,
                        symbols[  # pyrefly: ignore[bad-argument-type, bad-index]
                            n.args[0]
                        ],
                        Dyn,
                        n.args[1],
                        index_select,
                    )
                    for i in range(MAX_TENSOR_RANK)
                ]
            ),
        ]
    )

    return [Disj([c2, c3])], counter

