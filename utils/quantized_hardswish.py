
def quantized_hardswish(g: jit_utils.GraphContext, x, op_scale, op_zero_point):
    x, _, _, _ = symbolic_helper.dequantize_helper(g, x)

    output = opset9.hardswish(g, x)

    return symbolic_helper.quantize_helper(g, output, op_scale, op_zero_point)


def quantized_hardswish(g: jit_utils.GraphContext, x, op_scale, op_zero_point):
    x, _, _, _ = symbolic_helper.dequantize_helper(g, x)

    output = hardswish(g, x)

    return symbolic_helper.quantize_helper(g, output, op_scale, op_zero_point)

