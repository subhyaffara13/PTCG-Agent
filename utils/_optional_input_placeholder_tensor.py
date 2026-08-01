
def _optional_input_placeholder_tensor(g):
    n = g.op("prim::Constant")
    n.setType(_C.OptionalType.ofTensor())
    return n

