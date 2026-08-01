
def torch_linear_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    weight_dims, counter = gen_tensor_dims(2, counter)
    equality_constraint = BinConstraintT(
        symbols[n.args[1]],  # pyrefly: ignore[bad-index]
        TensorType(weight_dims),
        op_eq,
    )
    constraints, counter = linear_constraints(
        n, weight_dims[1], weight_dims[0], symbols, counter
    )
    return [equality_constraint] + constraints, counter

