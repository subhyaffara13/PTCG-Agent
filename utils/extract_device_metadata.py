from typing import Any

def extract_device_metadata(input: torch.device) -> dict[str, Any]:
    assert isinstance(input, torch.device)
    metadata: dict[str, Any] = {}
    metadata["device_type_value"] = f"{input.type}"
    metadata["device_index_value"] = input.index
    return metadata

