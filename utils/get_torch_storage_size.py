
def get_torch_storage_size(tensor: "torch.Tensor") -> int:
    """
    Taken from https://github.com/huggingface/safetensors/blob/08db34094e9e59e2f9218f2df133b7b4aaff5a99/bindings/python/py_src/safetensors/torch.py#L31C1-L41C59
    """
    try:
        from torch.distributed.tensor import DTensor

        if isinstance(tensor, DTensor):
            # this returns the size of the FULL tensor in bytes
            return tensor.nbytes
    except ImportError:
        pass

    try:
        # for torch 2.1 and above we can also handle tensor subclasses
        from torch.utils._python_dispatch import is_traceable_wrapper_subclass

        if is_traceable_wrapper_subclass(tensor):
            attrs, _ = tensor.__tensor_flatten__()  # type: ignore[attr-defined]
            return sum(get_torch_storage_size(getattr(tensor, attr)) for attr in attrs)
    except ImportError:
        # for torch version less than 2.1, we can fall back to original implementation
        pass

    try:
        return tensor.untyped_storage().nbytes()
    except AttributeError:
        # Fallback for torch==1.10
        try:
            return tensor.storage().size() * _get_dtype_size(tensor.dtype)
        except NotImplementedError:
            # Fallback for meta storage
            # On torch >=2.0 this is the tensor size
            return tensor.nelement() * _get_dtype_size(tensor.dtype)

