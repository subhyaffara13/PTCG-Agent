
def maxpool_inference_rule(
    n: Node,
    module_instance: torch.nn.MaxPool2d,
    symbols: _SymbolDict,
    constraints: list[Constraint],
    counter: int,
) -> tuple[list[Constraint], int]:
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    maxpool, counter = gen_tvar(counter)
    symbols[n] = maxpool
    input_var = symbols[n.args[0]]

    # dim vars
    [d1, d2, d3, d4], counter = gen_tensor_dims(MAX_TENSOR_RANK, counter)

    c1 = BinConstraintT(input_var, TensorType([d1, d2, d3, d4]), op_matching)

    c2 = CalcMaxPool(
        maxpool,
        input_var,  # pyrefly: ignore[bad-argument-type]
        module_instance.kernel_size,
        module_instance.padding,
        module_instance.stride,
        module_instance.dilation,
        [d1, d2, d3, d4],
    )

    nat_constraints = gen_nat_constraints([d1, d2, d3, d4])

    return [c1, c2, *nat_constraints], counter

