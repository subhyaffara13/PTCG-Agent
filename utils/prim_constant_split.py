
def prim_constant_split(g: jit_utils.GraphContext, self, split_size, dim):
    size = symbolic_helper._get_tensor_dim_size(self, dim)
    if size is None:
        return symbolic_helper._unimplemented(
            "prim::ConstantSplit", "unknown dimension size", self
        )
    splits = [split_size] * (size // split_size)
    leftover = size % split_size
    if leftover:
        splits.append(leftover)
    return g.op("Split", self, split_i=splits, axis_i=dim, outputs=len(splits))

