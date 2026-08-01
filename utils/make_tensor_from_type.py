
def make_tensor_from_type(inp_type: torch._C.TensorType):
    size = inp_type.sizes()
    stride = inp_type.strides()
    device = inp_type.device()
    dtype = inp_type.dtype()
    if size is None:
        raise AssertionError("make_tensor_from_type: 'size' is None (inp_type.sizes() returned None)")
    if stride is None:
        raise AssertionError("make_tensor_from_type: 'stride' is None (inp_type.strides() returned None)")
    if device is None:
        raise AssertionError("make_tensor_from_type: 'device' is None (inp_type.device() returned None)")
    if dtype is None:
        raise AssertionError("make_tensor_from_type: 'dtype' is None (inp_type.dtype() returned None)")
    return torch.empty_strided(size=size, stride=stride, device=device, dtype=dtype)

