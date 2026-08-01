
def _from_ort_value(value: ort.OrtValue) -> torch.Tensor:
    if value.element_type() in (
        ir.DataType.BFLOAT16,
        ir.DataType.FLOAT8E4M3FN,
        ir.DataType.FLOAT8E4M3FNUZ,
        ir.DataType.FLOAT8E5M2,
        ir.DataType.FLOAT8E5M2FNUZ,
    ):
        # This requires ONNX Runtime 1.21 or newer
        try:
            return torch.from_dlpack(value._get_c_value())
        except Exception as e:
            raise RuntimeError(
                "Failed to convert OrtValue to torch.Tensor. "
                "Please ensure that ONNX Runtime is built with DLPack support or is the latest version"
            ) from e
    return torch.from_numpy(value.numpy())

