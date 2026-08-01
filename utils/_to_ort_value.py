
def _to_ort_value(input: torch.Tensor | int | float | str | bool) -> ort.OrtValue:
    """Convert a PyTorch tensor to an ONNX Runtime OrtValue."""
    import numpy as np
    import onnxruntime as ort

    from torch.onnx._internal.exporter import _core

    if isinstance(input, (int, float, str, bool)):
        # Convert scalar values to OrtValue
        dtype_mapping = {
            int: np.int64,
            float: np.float32,
        }
        # pyrefly: ignore [bad-argument-type, no-matching-overload]
        dtype = dtype_mapping.get(type(input))
        return ort.OrtValue.ortvalue_from_numpy(np.array(input, dtype=dtype))

    if input.dtype == torch.bfloat16 or input.dtype in _NP_UNSUPPORTED_DTYPES_8BIT:
        if hasattr(ort.OrtValue, "ortvalue_from_numpy_with_onnx_type"):
            # This requires ONNX Runtime 1.21 or newer
            if input.dtype == torch.bfloat16:
                uint_type = torch.uint16
            else:
                uint_type = torch.uint8
            onnx_type = _core.torch_dtype_to_onnx_dtype(input.dtype)
            # Make tensor contiguous to ensure view() works
            input = input.contiguous()
            return ort.OrtValue.ortvalue_from_numpy_with_onnx_type(
                input.view(uint_type).numpy(force=True), onnx_element_type=onnx_type
            )
        raise RuntimeError(
            f"Failed to convert tensor of type '{input.dtype}' to OrtValue. "
            "Please ensure that ONNX Runtime is built with DLPack support or is the latest version"
        )
    # TODO(#151064): Use dlpack when ORT properly supports it
    return ort.OrtValue.ortvalue_from_numpy(input.numpy(force=True))

