
def _is_complete(tensor: torch.Tensor) -> bool:
    return tensor.data_ptr() == storage_ptr(tensor) and tensor.nelement() * _SIZE[
        tensor.dtype
    ] == storage_size(tensor)


def _is_complete(tensor: "torch.Tensor") -> bool:
    """
    Taken from https://github.com/huggingface/safetensors/blob/079781fd0dc455ba0fe851e2b4507c33d0c0d407/bindings/python/py_src/safetensors/torch.py#L80
    """
    try:
        # for torch 2.1 and above we can also handle tensor subclasses
        from torch.utils._python_dispatch import is_traceable_wrapper_subclass

        if is_traceable_wrapper_subclass(tensor):
            attrs, _ = tensor.__tensor_flatten__()  # type: ignore[attr-defined]
            return all(_is_complete(getattr(tensor, attr)) for attr in attrs)
    except ImportError:
        # for torch version less than 2.1, we can fall back to original implementation
        pass

    return tensor.data_ptr() == storage_ptr(tensor) and tensor.nelement() * _get_dtype_size(
        tensor.dtype
    ) == get_torch_storage_size(tensor)

