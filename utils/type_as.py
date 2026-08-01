
def type_as(g: jit_utils.GraphContext, self, other):
    self_dtype = symbolic_helper._try_get_scalar_type(self)
    other_dtype = symbolic_helper._try_get_scalar_type(other)
    if self_dtype == other_dtype and self_dtype is not None:
        return self
    if other_dtype is not None:
        return g.op(
            "Cast",
            self,
            to_i=other_dtype.onnx_type(),
        )

    raise errors.SymbolicValueError(
        "Unsupported: ONNX export of type_as for tensor "
        "of unknown dtype. Please check if the dtype of the "
        "parameter passed to the type_as function is correct.",
        other,
    )

