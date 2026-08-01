
def _get_json_schema_type(param_type: type) -> dict[str, str]:
    type_mapping = {
        int: {"type": "integer"},
        float: {"type": "number"},
        str: {"type": "string"},
        bool: {"type": "boolean"},
        type(None): {"type": "null"},
        Any: {},
    }
    if is_vision_available():
        type_mapping[Image] = {"type": "image"}
    if is_torch_available():
        import torch

        type_mapping[torch.Tensor] = {"type": "audio"}
    return type_mapping.get(param_type, {"type": "object"})

