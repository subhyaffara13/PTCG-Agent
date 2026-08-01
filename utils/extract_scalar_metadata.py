
def extract_scalar_metadata(device_type: str, input: Any) -> dict[str, Any]:
    assert isinstance(input, supported_scalar_types())
    metadata: dict[str, Any] = {}
    metadata["is_dynamic"] = False
    # Scalar tensor
    metadata["device_type"] = device_type
    metadata["device_index"] = -1 if device_type == "cpu" else 0
    type_to_torch_dtype = supported_builtin_dtype_torch_dtype()
    metadata["dtype"] = f"{type_to_torch_dtype[type(input)]}"
    metadata["scalar_value"] = input
    return metadata

