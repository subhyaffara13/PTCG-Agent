
def transpose_inference_rule(n: Node):
    """
    We check that dimensions for the transpose operations
    are within range of the tensor type of the node
    """
    if n.target is torch.transpose:
        if not isinstance(n.args[0], Node):
            raise AssertionError(f"Expected Node, got {type(n.args[0])}")
        t = n.args[0].type

        if not isinstance(n.args[1], int):
            raise AssertionError(f"Expected int, got {type(n.args[1])}")
        if not isinstance(n.args[2], int):
            raise AssertionError(f"Expected int, got {type(n.args[2])}")
        dim1, dim2 = n.args[1], n.args[2]

        if t == Dyn:
            n.type = Dyn
            return n.type

        elif isinstance(t, TensorType):
            if 0 <= dim1 < len(t.__args__) and 0 <= dim2 < len(t.__args__):
                new_type = list(t.__args__)
                new_type[dim1], new_type[dim2] = new_type[dim2], new_type[dim1]
                final = TensorType(new_type)
                n.type = get_greatest_upper_bound(n.type, final)
                return n.type
            else:
                raise TypeError(
                    f"Cannot transpose {dim1} and {dim2} in type {t} for node {n}"
                )
        else:
            raise TypeError(
                f"Cannot transpose {dim1} and {dim2} in type {t} for node {n}"
            )


def transpose_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    """
    Can be considered as a sequence of two index selects, so we generate constraints accordingly
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    if not isinstance(n.args[1], int):
        raise AssertionError(f"Expected int, got {type(n.args[1])}")
    if not isinstance(n.args[2], int):
        raise AssertionError(f"Expected int, got {type(n.args[2])}")

    output, counter = gen_tvar(counter)
    symbols[n] = output

    from_arg = symbols[n.args[0]]
    if not isinstance(from_arg, TVar):
        raise AssertionError(f"Expected TVar, got {type(from_arg)}")

    # input and output are dyn
    is_dyn = Conj(
        [BinConstraintT(from_arg, Dyn, op_eq), BinConstraintT(output, Dyn, op_eq)]
    )

    # or input is a tensor and we actually do the replacement
    c3 = Disj(
        [
            Transpose(i + 1, from_arg, n.args[1], n.args[2], output)
            for i in range(MAX_TENSOR_RANK)
        ]
    )

    return [Disj([is_dyn, c3])], counter

