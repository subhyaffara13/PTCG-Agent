
def _handle_reduce_dim_none(g: jit_utils.GraphContext, self, op_name):
    rank = _get_tensor_rank(self)
    if rank is not None and any(
        _get_tensor_dim_size(self, i) == 0 for i in range(rank)
    ):
        # If input tensor is empty, according to ONNX ReduceSum definition,
        # set keepdims=1 so that the resulted tensor has the same rank as the input.
        return g.op(op_name, self, keepdims_i=1)
    return g.op(op_name, self, keepdims_i=0)

