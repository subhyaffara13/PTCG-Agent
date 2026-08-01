
def quantized_add_relu(g: jit_utils.GraphContext, x, y, op_scale, op_zero_point):
    x, _, _, _ = symbolic_helper.dequantize_helper(g, x)
    y, _, _, _ = symbolic_helper.dequantize_helper(g, y)

    output = opset9.add(g, x, y)
    output = opset9.relu(g, output)

    return symbolic_helper.quantize_helper(g, output, op_scale, op_zero_point)

