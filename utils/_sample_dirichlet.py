
def _sample_dirichlet(g: jit_utils.GraphContext, self, generator):
    return symbolic_helper._onnx_unsupported("_sample_dirichlet", self)

