
def _parse_onnx_op(op: torch._ops.OpOverload) -> tuple[str, int]:
    """Parse the ONNX custom op overload name to get the op type and opset version."""
    name = op.name()[len("onnx::") :]
    name, _, opset = name.partition(".opset")
    return name, int(opset)

