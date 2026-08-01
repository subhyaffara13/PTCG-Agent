
def prim_shape(g: jit_utils.GraphContext, self):
    return g.op("Shape", self)

