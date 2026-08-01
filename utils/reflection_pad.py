
def reflection_pad(g: jit_utils.GraphContext, input, padding):
    mode = "reflect"
    paddings = _prepare_onnx_paddings(g, input, padding)
    return g.op("Pad", input, paddings, mode_s=mode)


def reflection_pad(g: jit_utils.GraphContext, input, padding):
    mode = "reflect"
    padding = _convert_padding_node(padding)
    # pyrefly: ignore [bad-argument-type]
    paddings = _prepare_onnx_paddings(symbolic_helper._get_tensor_rank(input), padding)
    return symbolic_helper._op_with_optional_float_cast(
        g, "Pad", input, pads_i=paddings, mode_s=mode, opset_before=11
    )

