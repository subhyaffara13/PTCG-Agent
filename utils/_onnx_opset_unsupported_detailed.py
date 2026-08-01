
def _onnx_opset_unsupported_detailed(
    op_name: str,
    current_opset: int,
    supported_opset: int,
    reason: str,
    value: _C.Value | None = None,
) -> NoReturn:
    message = (
        f"Unsupported: ONNX export of {op_name} in "
        f"opset {current_opset}. {reason}. Please try opset version {supported_opset}."
    )
    if isinstance(value, _C.Value):
        raise errors.SymbolicValueError(
            message,
            value,
        )
    raise errors.OnnxExporterError(message)

