
def _reshape_to_1d_tensor(opset: onnxscript.values.Opset, arg: ir.Value) -> ir.Value:
    """Reshape the input to a 1D tensor."""

    return opset.Reshape(
        arg, opset.Constant(value=ir.tensor([-1], dtype=ir.DataType.INT64))
    )

