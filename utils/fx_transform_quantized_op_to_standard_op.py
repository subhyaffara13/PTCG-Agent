
def fx_transform_quantized_op_to_standard_op(
    gm: torch.fx.GraphModule, node: torch.fx.Node
) -> torch.fx.Node:
    global _SCALE, _ZERO_POINT, _INPUT_Q_DTYPE

    if not isinstance(node.target, torch._ops.OpOverload):
        raise AssertionError(f"expected OpOverload, got {type(node.target).__name__}")
    opname, overload = node.target._opname, node.target._overloadname

    key = f"{opname}.{overload}"
    opname_to_transform_f = {
        "conv1d.new": _transform_conv_with_packedparam,
        "conv1d_relu.new": _transform_conv_with_packedparam,
        "conv1d.default": _transform_conv_with_packedparam,
        "conv1d_relu.default": _transform_conv_with_packedparam,
        "conv2d.new": _transform_conv_with_packedparam,
        "conv2d_relu.new": _transform_conv_with_packedparam,
        "conv2d.default": _transform_conv_with_packedparam,
        "conv2d_relu.default": _transform_conv_with_packedparam,
        "linear.default": _transform_linear_with_packedparam,
        "linear_relu.default": _transform_linear_with_packedparam,
        "add.default": _transform_op_where_last_two_arguments_are_scale_and_zero_point,
        "add_relu.default": _transform_op_where_last_two_arguments_are_scale_and_zero_point,
        "mul.default": _transform_op_where_last_two_arguments_are_scale_and_zero_point,
        "mul_relu.default": _transform_op_where_last_two_arguments_are_scale_and_zero_point,
        "softmax.default": _transform_op_where_last_two_arguments_are_scale_and_zero_point,
        "cat.default": _transform_op_where_last_two_arguments_are_scale_and_zero_point,
        "hardswish.default": _transform_op_where_last_two_arguments_are_scale_and_zero_point,
        "batch_norm2d.default": _transform_batch_norm,
        "mul.Scalar": _transform_scalar_arithmetic,
        "add.Scalar": _transform_scalar_arithmetic,
    }

    if f"{key}" not in opname_to_transform_f:
        raise RuntimeError(f"Unsupported quantized op during transformation: {key}")

    op_res_node, scale_node, zero_point_node = opname_to_transform_f[f"{key}"](gm, node)

    # Add fused activation layer.
    op_res_node = insert_fused_activation_node(gm, opname, op_res_node)
    _SCALE, _ZERO_POINT = scale_node, zero_point_node

    if _INPUT_Q_DTYPE is None:
        raise AssertionError("_INPUT_Q_DTYPE should not be None")
    qmin_node, qmax_node = insert_qmin_qmax_node(gm, _INPUT_Q_DTYPE)
    q_fx_node = insert_quantized_node(
        gm,
        op_res_node,
        scale_node,
        zero_point_node,
        qmin_node,
        qmax_node,
        _INPUT_Q_DTYPE,
        torch.per_tensor_affine,
    )
    dq_fx_node = insert_dequantized_node(
        gm,
        q_fx_node,
        scale_node,
        zero_point_node,
        qmin_node,
        qmax_node,
        _INPUT_Q_DTYPE,
        None,
        torch.per_tensor_affine,
    )
    return dq_fx_node

