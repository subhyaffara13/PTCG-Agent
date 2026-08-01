
def quantized_layer_norm(
    g: jit_utils.GraphContext,
    x,
    normalized_shape,
    weight,
    bias,
    eps,
    op_scale,
    op_zero_point,
):
    x, _, _, _ = symbolic_helper.dequantize_helper(g, x)

    output = opset9.layer_norm(g, x, normalized_shape, weight, bias, eps, False)

    return symbolic_helper.quantize_helper(g, output, op_scale, op_zero_point)


def quantized_layer_norm(
    g: jit_utils.GraphContext,
    x,
    normalized_shape,
    weight,
    bias,
    eps,
    op_scale,
    op_zero_point,
):
    x, _, _, _ = symbolic_helper.dequantize_helper(g, x)

    output = layer_norm(g, x, normalized_shape, weight, bias, eps, False)

    return symbolic_helper.quantize_helper(g, output, op_scale, op_zero_point)

