
def _onnx_opset_unsupported(
    op_name: str,
    current_opset: int,
    supported_opset: int,
    value: _C.Value | None = None,
) -> NoReturn:
    message = (
        f"Unsupported: ONNX export of {op_name} in opset {current_opset}. "
        f"Please try opset version {supported_opset}."
    )
    if isinstance(value, _C.Value):
        raise errors.SymbolicValueError(
            message,
            value,
        )
    raise errors.OnnxExporterError(message)

