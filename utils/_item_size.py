
def _item_size(item: WriteItem) -> int:
    size = 1
    if item.tensor_data is None:
        raise AssertionError("WriteItem tensor_data must not be None")
    # can't use math.prod as PT needs to support older python
    for s in item.tensor_data.size:
        size *= s

    dtype = item.tensor_data.properties.dtype
    return size * torch._utils._element_size(dtype)

