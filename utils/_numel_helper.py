
def _numel_helper(g: jit_utils.GraphContext, self):
    shape = g.op("Shape", self)
    return g.op("ReduceProd", shape, keepdims_i=0)

