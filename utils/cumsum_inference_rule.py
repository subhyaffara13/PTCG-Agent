
def cumsum_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    """
    Input and output shapes should be equal
    We should verify that the index is valid
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    arg_1 = n.args[1] if len(n.args) > 1 else n.kwargs["dim"]
    if not isinstance(arg_1, int):
        raise AssertionError(f"Expected int, got {type(arg_1)}")

    output, counter = gen_tvar(counter)
    symbols[n] = output
    input = symbols[n.args[0]]

    input_dyn = BinConstraintT(input, Dyn, op_eq)
    output_dyn = BinConstraintT(output, Dyn, op_eq)
    c1 = Conj([input_dyn, output_dyn])
    c2 = []
    for i in range(1, MAX_TENSOR_RANK + 1):
        new_dims, counter = gen_tensor_dims(i, counter)

        nat_constraints = gen_nat_constraints(new_dims)

        c_tensor_i = Conj(
            [
                BinConstraintT(input, TensorType(new_dims), op_eq),
                BinConstraintT(output, TensorType(new_dims), op_eq),
            ]
            + [range_check(arg_1, i)]
            + nat_constraints
        )

        c2.append(c_tensor_i)
    dyn_or_tensor = Disj([c1, Disj(c2)])
    return [dyn_or_tensor], counter

