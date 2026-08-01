
def linear_constraints(
    n: Node,
    in_features: int | DVar,
    out_features: int | DVar,
    symbols: _SymbolDict,
    counter: int,
) -> tuple[list[Constraint], int]:
    linear_output, counter = gen_tvar(counter)
    symbols[n] = linear_output
    linear_input = symbols[n.args[0]]  # pyrefly: ignore[bad-index]

    input_dyn = BinConstraintT(linear_input, Dyn, op_eq)
    output_dyn = BinConstraintT(linear_output, Dyn, op_eq)

    c1 = Conj([input_dyn, output_dyn])

    c2 = []
    for i in range(1, MAX_TENSOR_RANK + 1):
        new_dims_rhs_1, counter = gen_tensor_dims(i, counter)
        new_dims_rhs_2, counter = gen_tensor_dims(i, counter)

        nat_constraints = gen_nat_constraints(new_dims_rhs_1 + new_dims_rhs_2)

        c_tensor_i = Conj(
            [
                BinConstraintT(linear_input, TensorType(new_dims_rhs_1), op_eq),
                BinConstraintT(linear_output, TensorType(new_dims_rhs_2), op_eq),
            ]
            + add_linear_constraints(
                new_dims_rhs_1, new_dims_rhs_2, in_features, out_features
            )
            + nat_constraints
        )
        c2.append(c_tensor_i)
    return [Disj([c1, Disj(c2)])], counter

