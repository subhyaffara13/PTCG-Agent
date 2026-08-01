
def quantized_group_norm(
    g: jit_utils.GraphContext,
    x,
    num_groups,
    weight,
    bias,
    eps,
    op_scale,
    op_zero_point,
):
    x, _, _, _ = symbolic_helper.dequantize_helper(g, x)

    output = opset9.group_norm(g, x, num_groups, weight, bias, eps, False)

    return symbolic_helper.quantize_helper(g, output, op_scale, op_zero_point)

