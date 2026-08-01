
def linalg_det(g: jit_utils.GraphContext, self):
    return g.op("Det", self)

