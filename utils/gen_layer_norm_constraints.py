
def gen_layer_norm_constraints(
    n: Node, normalized_shape: Sequence[int], symbols: _SymbolDict, counter: int
) -> tuple[list[Constraint], int]:
    output, counter = gen_tvar(counter)
    symbols[n] = output
    input = symbols[n.args[0]]  # pyrefly: ignore[bad-index]

    input_dyn = BinConstraintT(input, Dyn, op_eq)
    output_dyn = BinConstraintT(output, Dyn, op_eq)

    c1 = Conj([input_dyn, output_dyn])

    c2 = []
    for i in range(1, MAX_TENSOR_RANK + 1):
        new_dims_rhs, counter = gen_tensor_dims(i, counter)
        nat_constraints = gen_nat_constraints(new_dims_rhs)

        c_tensor_i = Conj(
            [
                BinConstraintT(input, TensorType(new_dims_rhs), op_eq),
                BinConstraintT(output, TensorType(new_dims_rhs), op_eq),
            ]
            + add_layer_norm_constraints(new_dims_rhs, list(normalized_shape))
            + nat_constraints
        )
        c2.append(c_tensor_i)
    return [Disj([c1, Disj(c2)])], counter

