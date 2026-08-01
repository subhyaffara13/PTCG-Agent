
def _onnx_unsupported(op_name: str, value: _C.Value | None = None) -> NoReturn:
    message = (
        f"Unsupported: ONNX export of operator {op_name}. "
        f"Please feel free to request support or submit a pull request "
        f"on PyTorch GitHub: {_constants.PYTORCH_GITHUB_ISSUES_URL}"
    )
    if isinstance(value, _C.Value):
        raise errors.SymbolicValueError(
            message,
            value,
        )
    raise errors.OnnxExporterError(message)

