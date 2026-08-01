
def _is_onnx_constant(value: _C.Value):
    """Whether a Value is an ONNX constant."""
    return value.node().kind() == "onnx::Constant"

