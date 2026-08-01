
def _is_onnx_op(op: Any) -> bool:
    """Whether the op overload is an ONNX custom op implemented with PyTorch."""
    if not isinstance(op, torch._ops.OpOverload):
        return False
    return op.name().startswith("onnx::")

