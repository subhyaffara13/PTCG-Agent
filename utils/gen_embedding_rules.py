
def gen_embedding_rules(
    n: Node, symbols: _SymbolDict, embedding_dim: int | DVar, counter: int
) -> tuple[list[Constraint], int]:
    embedding_output, counter = gen_tvar(counter)
    symbols[n] = embedding_output
    embedding_input = symbols[n.args[0]]  # pyrefly: ignore[bad-index]

    input_dyn = BinConstraintT(embedding_input, Dyn, op_eq)
    output_dyn = BinConstraintT(embedding_output, Dyn, op_eq)

    c1 = Conj([input_dyn, output_dyn])
    c2 = []

    for i in range(1, MAX_TENSOR_RANK):
        new_dims, counter = gen_tensor_dims(i, counter)
        nat_constraints = gen_nat_constraints(new_dims)

        # we consider all tensor sizes and append embedding_dim to the end of the output dimension in all cases
        c_tensor_i = Conj(
            [
                BinConstraintT(embedding_input, TensorType(new_dims), op_eq),
                BinConstraintT(
                    embedding_output, TensorType(new_dims + [embedding_dim]), op_eq
                ),
            ]
            + nat_constraints
        )
        c2.append(c_tensor_i)

    return [Disj([c1, Disj(c2)])], counter

