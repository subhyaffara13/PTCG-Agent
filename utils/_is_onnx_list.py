
def _is_onnx_list(value):
    return isinstance(value, Iterable) and not isinstance(
        value, (str, bytes, torch.Tensor)
    )

