
def _end_ptr(tensor: torch.Tensor) -> int:
    if tensor.nelement():
        stop = tensor.view(-1)[-1].data_ptr() + _SIZE[tensor.dtype]
    else:
        stop = tensor.data_ptr()
    return stop


def _end_ptr(tensor: torch.Tensor) -> int:
    # extract the end of the pointer if the tensor is a slice of a bigger tensor
    if tensor.nelement():
        stop = tensor.view(-1)[-1].data_ptr() + tensor.element_size()
    else:
        stop = tensor.data_ptr()
    return stop


def _end_ptr(tensor: torch.Tensor) -> int:
    if tensor.nelement():
        stop = tensor.view(-1)[-1].data_ptr() + tensor.element_size()
    else:
        stop = tensor.data_ptr()
    return stop


def _end_ptr(tensor: "torch.Tensor") -> int:
    """
    Taken from https://github.com/huggingface/safetensors/blob/079781fd0dc455ba0fe851e2b4507c33d0c0d407/bindings/python/py_src/safetensors/torch.py#L23.
    """
    if tensor.nelement():
        stop = tensor.view(-1)[-1].data_ptr() + _get_dtype_size(tensor.dtype)
    else:
        stop = tensor.data_ptr()
    return stop

