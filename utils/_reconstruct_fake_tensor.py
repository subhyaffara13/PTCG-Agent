import json

def _reconstruct_fake_tensor(
    serialized_tensor_meta: bytes, is_parameter: bool
) -> FakeTensor:
    # Deserialize the bytes into a TensorMeta
    json_tensor_meta = json.loads(serialized_tensor_meta.decode("utf-8"))
    tensor_meta = _dict_to_dataclass(TensorMeta, json_tensor_meta)
    # Find the current fake mode
    if _CURRENT_DESERIALIZER is None:
        raise AssertionError("Need access to current deserializer state")
    fake_tensor = _CURRENT_DESERIALIZER.deserialize_tensor_meta(tensor_meta)
    if is_parameter:
        fake_tensor = torch.nn.Parameter(fake_tensor)  # type: ignore[assignment]
    # pyrefly: ignore [bad-return]
    return fake_tensor

