
def torch_dim_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    my_dim, counter = gen_dvar(counter)
    symbols[n] = my_dim
    input = symbols[n.args[0]]

    input_dyn = BinConstraintT(input, Dyn, op_eq)
    output_dyn = BinConstraintD(my_dim, Dyn, op_eq)

    c1 = []

    for i in range(1, MAX_TENSOR_RANK + 1):
        new_dims_rhs_1, counter = gen_tensor_dims(i, counter)

        c_tensor_i = Conj(
            [
                BinConstraintT(input, TensorType(new_dims_rhs_1), op_eq),
                BinConstraintD(my_dim, i, op_eq),
            ]
        )
        c1.append(c_tensor_i)

    return [Disj([Conj([input_dyn, output_dyn]), Disj(c1)])], counter

