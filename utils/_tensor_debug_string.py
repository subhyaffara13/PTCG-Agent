
def _tensor_debug_string(tensor, attributes, tensor_memo=None) -> str:
    """Convert tensor to debug string representation."""

    if isinstance(tensor, torch.Tensor):
        tensor_debug_str = f"{dtype_abbrs[tensor.dtype]}{_stringify_shape(tensor.shape)}{_stringify_attributes(tensor, attributes)}"
        id_str = f"${tensor_memo._id(tensor)}" if tensor_memo is not None else ""
        if isinstance(tensor, torch.distributed.tensor.DTensor):
            # omitted device mesh
            return f"dt{id_str}: {tensor_debug_str}| {_stringify_dtensor_spec(tensor._spec)}"
        elif isinstance(tensor, FakeTensor):
            return f"ft{id_str}: {tensor_debug_str}"
        else:
            return f"t{id_str}: {tensor_debug_str}"
    else:
        raise RuntimeError(f"Unsupported tensor type: {type(tensor)}")

