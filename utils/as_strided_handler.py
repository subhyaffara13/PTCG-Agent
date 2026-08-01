
def as_strided_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
):
    args, kwargs = fill_defaults(op_call._schema, args, kwargs)
    if kwargs:
        raise AssertionError
    tensor, size, stride, storage_offset = args
    if (
        tensor.size() == tuple(size)
        and tensor.stride() == tuple(stride)
        and (storage_offset is None or tensor.storage_offset() == storage_offset)
    ):
        return torch.ops.aten.alias.default(tensor)
    raise RuntimeError("as_strided not supported with DTensor")

