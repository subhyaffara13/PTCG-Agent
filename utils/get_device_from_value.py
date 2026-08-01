
def get_device_from_value(value: _C.Value) -> torch.device | None:
    if not _is_tensor(value):
        return None
    tensor_type = typing.cast(_C.TensorType, value.type())
    return tensor_type.device()

