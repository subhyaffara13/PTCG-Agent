
def _standard_gamma(concentration):
    return torch._standard_gamma(concentration)


def _standard_gamma(g: jit_utils.GraphContext, self, generator):
    return symbolic_helper._onnx_unsupported("_standard_gamma", self)

