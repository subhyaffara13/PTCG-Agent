
def prim_constant_chunk(g: jit_utils.GraphContext, self, chunks, dim):
    input_shape = g.op("Shape", self)
    axis = g.op("Constant", value_t=torch.tensor([dim], dtype=torch.long))
    input_shape_dim = g.op("Gather", input_shape, axis, axis_i=0)
    start = g.op("Constant", value_t=torch.tensor([0], dtype=torch.long))
    chunk_size = g.op("Constant", value_t=torch.tensor([chunks], dtype=torch.long))
    chunk_size_minus_1 = g.op(
        "Constant", value_t=torch.tensor([chunks - 1], dtype=torch.long)
    )
    input_shape_dim_shift = g.op("Add", input_shape_dim, chunk_size_minus_1)
    chunk_dim = g.op("Div", input_shape_dim_shift, chunk_size)
    res = []
    for i in range(chunks):
        index = g.op("Constant", value_t=torch.tensor([i + 1], dtype=torch.long))
        end = g.op("Mul", chunk_dim, index)
        res.append(g.op("Slice", self, start, end, axis))
        start = end
    return res


def prim_constant_chunk(g: jit_utils.GraphContext, self, chunks, dim):
    dim_size = symbolic_helper._get_tensor_dim_size(self, dim)
    if dim_size is None:
        return symbolic_helper._unimplemented(
            "prim::ConstantChunk", "unknown dimension size", self
        )
    split_size = (dim_size + chunks - 1) // chunks
    return prim_constant_split(g, self, split_size, dim)

