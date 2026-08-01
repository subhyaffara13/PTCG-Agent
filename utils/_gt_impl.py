
def _gt_impl(g: jit_utils.GraphContext, input, other):
    if symbolic_helper._is_bool(input) and symbolic_helper._is_bool(other):
        input = g.op("Cast", input, to_i=_C_onnx.TensorProtoDataType.INT32)
        other = g.op("Cast", other, to_i=_C_onnx.TensorProtoDataType.INT32)
    return g.op("Greater", input, other)

