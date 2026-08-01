
def detach(g: jit_utils.GraphContext, input):
    # Erase aten::detach nodes because ONNX is inference only
    return input

