
def quantized_linear_relu(
    g: jit_utils.GraphContext, q_input, q_weight, bias, op_scale, op_zero_point
):
    input, input_scale, _, _ = symbolic_helper.dequantize_helper(g, q_input)
    weight, weight_scale, _, _ = symbolic_helper.dequantize_helper(g, q_weight)
    q_bias = symbolic_helper.requantize_bias_helper(g, bias, input_scale, weight_scale)
    bias, _, _, _ = symbolic_helper.dequantize_helper(g, q_bias)

    output = opset9.linear(g, input, weight, bias)
    output = opset9.relu(g, output)

    return symbolic_helper.quantize_helper(g, output, op_scale, op_zero_point)


def quantized_linear_relu(
    g: jit_utils.GraphContext, q_input, q_weight, bias, op_scale, op_zero_point
):
    input, input_scale, _, _ = symbolic_helper.dequantize_helper(g, q_input)
    weight, weight_scale, _, axis = symbolic_helper.dequantize_helper(g, q_weight)
    q_bias = symbolic_helper.requantize_bias_helper(
        g, bias, input_scale, weight_scale, axis
    )
    bias, _, _, _ = symbolic_helper.dequantize_helper(g, q_bias)

    output = opset9.linear(g, input, weight, bias)
    output = opset9.relu(g, output)

    return symbolic_helper.quantize_helper(g, output, op_scale, op_zero_point)

