
def tensor_attr_unsupported_getter(func, *args, **kwargs) -> None:
    if func is torch.ops.aten.size.default:
        raise RuntimeError(
            "NestedTensor does not support directly calling torch.ops.aten.size; "
            "please use `nested_tensor.size()` instead."
        )

