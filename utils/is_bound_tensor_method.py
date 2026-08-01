
def is_bound_tensor_method(value: object) -> bool:
    return bool(
        callable(value)
        and not torch._dynamo.utils.object_has_getattribute(value)
        and hasattr(value, "__self__")
        and isinstance(value.__self__, torch.Tensor)
        and getattr(value.__self__, value.__name__, None)
    )

