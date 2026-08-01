
def _cast_to_type(g: jit_utils.GraphContext, input, to_type):
    if to_type is None:
        return input
    return g.op("Cast", input, to_i=symbolic_helper.cast_pytorch_to_onnx[to_type])

