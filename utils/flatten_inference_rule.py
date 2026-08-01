
def flatten_inference_rule(n: Node):
    """
    Applies the flatten shape information to the input then gets the
    greatest upper bound of the resulting type and the existing type
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")

    # set the default start and end dims
    start_dim = 1
    end_dim = -1

    if len(n.args) > 1:
        if not isinstance(n.args[1], int):
            raise AssertionError(f"Expected int, got {type(n.args[1])}")
        start_dim = n.args[1]

    if len(n.args) > 2:
        if not isinstance(n.args[2], int):
            raise AssertionError(f"Expected int, got {type(n.args[2])}")
        end_dim = n.args[2]

    if n.args[0].type == Dyn and isinstance(n.type, TensorType):
        n.args[0].type = expand_to_tensor_dim(n.args[0].type, len(n.type.__args__))

    if isinstance(n.args[0].type, TensorType):
        output_type = flatten_check(n.args[0].type, start_dim, end_dim)
        n.type = get_greatest_upper_bound(output_type, n.type)

    return n.type


def flatten_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")

    # generate the new variable
    flattened, counter = gen_tvar(counter)
    symbols[n] = flattened

    input = symbols[n.args[0]]

    # set the default start and end dims
    start_dim = 1
    end_dim = -1

    if len(n.args) > 1:
        if not isinstance(n.args[1], int):
            raise AssertionError(f"Expected int, got {type(n.args[1])}")
        start_dim = n.args[1]

    if len(n.args) > 2:
        if not isinstance(n.args[2], int):
            raise AssertionError(f"Expected int, got {type(n.args[2])}")
        end_dim = n.args[2]

    c1 = BinConstraintT(input, Dyn, op_eq)
    c2 = BinConstraintT(flattened, Dyn, op_eq)
    both_dyn = Conj([c1, c2])

    const = []
    for i in range(1, MAX_TENSOR_RANK + 1):
        c, counter = generate_flatten_constraints(
            start_dim,
            end_dim,
            input,  # pyrefly: ignore[bad-argument-type]
            flattened,
            i,
            counter,
        )
        const.append(c)

    return [Disj([both_dyn, *const])], counter

