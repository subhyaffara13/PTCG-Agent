
def _reduce_op_symbolic(onnx_op_name):
    def symbolic(g, self, dim=None, keepdim=None):
        self = symbolic_helper._maybe_cast_reduce_op_input(g, self)
        if dim is None:
            # all-reduce path
            return symbolic_helper._handle_reduce_dim_none(g, self, onnx_op_name)
        else:
            keepdim = symbolic_helper._get_const(keepdim, "i", "keepdim")
            return g.op(onnx_op_name, self, dim, keepdims_i=keepdim)

    return symbolic

