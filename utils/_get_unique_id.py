
def _get_unique_id(tensor: "torch.Tensor") -> int | tuple[Any, ...]:
    """Returns a unique id for plain tensor
    or a (potentially nested) Tuple of unique id for the flattened Tensor
    if the input is a wrapper tensor subclass Tensor
    """

    try:
        from torch.distributed.tensor import DTensor

        if isinstance(tensor, DTensor):
            local_tensor = tensor.to_local()
            return local_tensor.storage().data_ptr()
    except ImportError:
        pass

    try:
        # for torch 2.1 and above we can also handle tensor subclasses
        from torch.utils._python_dispatch import is_traceable_wrapper_subclass

        if is_traceable_wrapper_subclass(tensor):
            attrs, _ = tensor.__tensor_flatten__()  # type: ignore[attr-defined]
            return tuple(_get_unique_id(getattr(tensor, attr)) for attr in attrs)

    except ImportError:
        # for torch version less than 2.1, we can fall back to original implementation
        pass

    if tensor.device.type == "xla" and is_torch_tpu_available():
        # NOTE: xla tensors don't have storage
        # use some other unique id to distinguish.
        # this is a XLA tensor, it must be created using torch_xla's
        # device. So the following import is safe:
        import torch_xla  # type: ignore[import]

        unique_id = torch_xla._XLAC._xla_get_tensor_id(tensor)
    else:
        unique_id = storage_ptr(tensor)

    return unique_id

