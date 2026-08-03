from typing import Any

def extract_tensor_list_metadata(
    dynamic: bool,
    input: list[torch.Tensor],
) -> dict[str, Any]:
    metadata_list = []
    for item in input:
        assert isinstance(item, torch.Tensor)
        metadata_list.append(extract_tensor_metadata(dynamic, item))

    metadata: dict[str, Any] = {}
    metadata["tensor_list"] = metadata_list
    return metadata

