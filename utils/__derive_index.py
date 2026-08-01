
def __derive_index(g: jit_utils.GraphContext, index, start, step):
    return g.op("Add", start, g.op("Mul", index, step))

