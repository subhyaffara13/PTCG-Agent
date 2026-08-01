
def embedding_inference_rule_functional(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")

    embedding_dim_weights = symbols[n.args[1]]  # pyrefly: ignore[bad-index]

    # will treat this as a static shape. So we will not use matching.
    weight_dims, counter = gen_tensor_dims(2, counter)
    equality_constraint = BinConstraintT(
        embedding_dim_weights, TensorType(weight_dims), op_eq
    )
    embedding_dim = weight_dims[1]
    constraints, counter = gen_embedding_rules(n, symbols, embedding_dim, counter)
    return [equality_constraint] + constraints, counter

