
def _reduce_fake_tensor(fake_tensor: FakeTensor):
    is_parameter = isinstance(fake_tensor, torch.nn.Parameter)
    tensor_meta = serialize_tensor_meta(fake_tensor)
    tensor_meta_bytes = json.dumps(
        _dataclass_to_dict(tensor_meta), cls=EnumEncoder
    ).encode("utf-8")
    return _reconstruct_fake_tensor, (tensor_meta_bytes, is_parameter)

