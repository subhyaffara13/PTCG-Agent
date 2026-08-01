
def unsafe_chunk(g: jit_utils.GraphContext, self, chunks, dim, _outputs=None):
    if _outputs is None:
        return g.op(
            "SplitToSequence",
            self,
            g.op("Constant", value_t=torch.tensor(1, dtype=torch.long)),
            axis_i=dim,
            keepdims_i=0,
        )

    size = symbolic_helper._get_tensor_dim_size(self, dim)
    if size is None:
        return symbolic_helper._unimplemented("unsafe_chunk", "unknown dimension size")
    split_size = (size + chunks - 1) // chunks
    splits = [split_size] * (size // split_size)
    leftover = size % split_size
    if leftover:
        splits.append(leftover)

    # TODO: So far we don"t have a module using this method. We"ll keep
    # this as a constant unless we see a request of dynamics in any
    # user's modules.
    splits = g.op("Constant", value_t=torch.tensor(splits, dtype=torch.long))
    return g.op("Split", self, splits, axis_i=dim, outputs=_outputs)


def unsafe_chunk(g: jit_utils.GraphContext, self, chunks, dim, _outputs=None):
    if _outputs is None:
        return symbolic_helper._onnx_opset_unsupported_detailed(
            "unsafe_chunk", 9, 11, "Dynamic number of outputs not supported", self
        )
    size = symbolic_helper._get_tensor_dim_size(self, dim)
    if size is None:
        return symbolic_helper._unimplemented(
            "unsafe_chunk", "unknown dimension size", self
        )
    split_size = (size + chunks - 1) // chunks
    splits = [split_size] * (size // split_size)
    leftover = size % split_size
    if leftover:
        splits.append(leftover)
    return g.op("Split", self, split_i=splits, axis_i=dim, outputs=_outputs)

