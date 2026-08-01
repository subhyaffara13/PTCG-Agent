
def prim_layout(g: jit_utils.GraphContext, self):
    # Always return 'torch.strided'. Other layout types are not supported by JIT 'TensorType'.
    # Layout class defined in 'c10/core/Layout.h'.
    return g.op("Constant", value_t=torch.tensor(0))

