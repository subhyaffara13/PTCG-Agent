
def conv2d_inference_rule(n: Node, module_instance):
    """
    Given a Conv2D instance and a node check the following conditions:
    - the input type can be expanded to a size 4 tensor: t =  (x_1, x_2, H, W)
    - the current node type can be expanded to a size 4 tensor: t' =  (x_1', x_2', x_3', x_4')
    - x_2 is consistent with the module's in_channels
    - let o = (x_1, out_channels, H_out, W_out)
    then the output is the greatest upper bound of o and the existing node type t'.
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    n.args[0].type = expand_to_tensor_dim(n.args[0].type, 4)
    arg_type = n.args[0].type
    curr_node_type = expand_to_tensor_dim(n.type, 4)

    if is_consistent(arg_type.__args__[1], module_instance.in_channels):
        w_in = arg_type.__args__[3]
        h_in = arg_type.__args__[2]
        h_out = calculate_out_dimension(h_in, module_instance, 0)
        w_out = calculate_out_dimension(w_in, module_instance, 1)
        new_type = TensorType(
            (arg_type.__args__[0], module_instance.out_channels, h_out, w_out)
        )
        gub = get_greatest_upper_bound(new_type, curr_node_type)
        n.type = gub
        return n.type
    else:
        raise TypeError(
            f"Cannot apply {module_instance} with input type {arg_type} and existing type {n.type} on {n}"
        )


def conv2d_inference_rule(
    n: Node,
    module_instance: Conv2d,
    symbols: _SymbolDict,
    constraints: list[Constraint],
    counter: int,
) -> tuple[list[Constraint], int]:
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")

    my_conv, counter = gen_tvar(counter)
    symbols[n] = my_conv
    input_var = symbols[n.args[0]]

    # dim vars
    [d1, d2, d3, d4], counter = gen_tensor_dims(MAX_TENSOR_RANK, counter)

    # c1 = Matching(input_var, TensorType([d1, d2, d3, d4]))
    c1 = BinConstraintT(input_var, TensorType([d1, d2, d3, d4]), op_matching)

    # c2 = DConsistency(module_instance.in_channels, d2)
    c2 = BinConstraintD(module_instance.in_channels, d2, op_consistency)

    c3 = CalcConv(
        my_conv,
        input_var,  # pyrefly: ignore[bad-argument-type]
        module_instance.out_channels,
        module_instance.kernel_size,  # pyrefly: ignore[bad-argument-type]
        module_instance.padding,  # pyrefly: ignore[bad-argument-type]
        module_instance.stride,  # pyrefly: ignore[bad-argument-type]
        module_instance.dilation,  # pyrefly: ignore[bad-argument-type]
        [d1, d2, d3, d4],
    )

    nat_constraints = gen_nat_constraints([d1, d2, d3, d4])

    return [c1, c2, c3, *nat_constraints], counter

