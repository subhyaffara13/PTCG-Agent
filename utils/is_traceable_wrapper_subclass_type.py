
def is_traceable_wrapper_subclass_type(t: type) -> TypeIs[type[TensorWithFlatten]]:
    """Same as above, but takes a type argument instead of an instance."""
    return (
        issubclass(t, torch.Tensor)
        and t is not torch.Tensor
        and hasattr(t, "__tensor_flatten__")
        and hasattr(t, "__tensor_unflatten__")
    )

