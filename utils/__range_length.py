
def __range_length(g: jit_utils.GraphContext, lo, hi, step):
    sub = g.op("Sub", hi, lo)
    div = g.op("Ceil", true_divide(g, sub, step))
    return g.op("Cast", div, to_i=_C_onnx.TensorProtoDataType.INT64)

