
def _unimplemented(op: str, msg: str, value: _C.Value | None = None) -> None:
    # For BC reasons, the behavior for Caffe2 does not raise exception for unimplemented operators
    if GLOBALS.operator_export_type == _C_onnx.OperatorExportTypes.ONNX:
        _onnx_unsupported(f"{op}, {msg}", value)

