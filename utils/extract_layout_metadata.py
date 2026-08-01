
def extract_layout_metadata(input: torch.layout) -> dict[str, Any]:
    assert isinstance(input, torch.layout)
    metadata: dict[str, Any] = {}
    metadata["layout_value"] = f"{input}"
    return metadata

