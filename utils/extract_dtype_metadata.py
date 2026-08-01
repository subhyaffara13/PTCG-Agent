
def extract_dtype_metadata(input: torch.dtype) -> dict[str, Any]:
    assert isinstance(input, torch.dtype)
    metadata: dict[str, Any] = {}
    metadata["dtype_value"] = f"{input}"
    return metadata

