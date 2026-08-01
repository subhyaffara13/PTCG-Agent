
def _should_aten_fallback(
    name: str, opset_version: int, operator_export_type: _C_onnx.OperatorExportTypes
) -> bool:
    # For all builds, if domain=="aten" and operator_export_type==ONNX_ATEN,
    #   an aten::ATen operator is created regardless of symbolics existence

    is_exportable_aten_op = registration.registry.is_registered_op(name, opset_version)
    is_onnx_aten_export = operator_export_type == _C_onnx.OperatorExportTypes.ONNX_ATEN
    is_aten_fallback_export = (
        operator_export_type == _C_onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK
    )

    if not name.startswith("aten::"):
        return False

    if is_onnx_aten_export or (is_aten_fallback_export and not is_exportable_aten_op):
        return True

    return False

