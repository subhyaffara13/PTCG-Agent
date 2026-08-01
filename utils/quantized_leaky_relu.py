
def quantized_leaky_relu(
    g: jit_utils.GraphContext, x, negative_slope, inplace, op_scale, op_zero_point
):
    x, _, _, _ = symbolic_helper.dequantize_helper(g, x)

    output = opset9.leaky_relu(g, x, negative_slope, inplace)

    return symbolic_helper.quantize_helper(g, output, op_scale, op_zero_point)

