
def logdet(g: jit_utils.GraphContext, input):
    return opset9.log(g, linalg_det(g, input))

