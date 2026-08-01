
def quantized_instance_norm(
    g: jit_utils.GraphContext,
    q_input,
    weight,
    bias,
    eps,
    op_scale,
    op_zero_point,
):
    input, _, _, _ = symbolic_helper.dequantize_helper(g, q_input)

    output = opset9.instance_norm(
        g, input, weight, bias, None, None, False, 0.0, eps, False
    )

    return symbolic_helper.quantize_helper(g, output, op_scale, op_zero_point)

