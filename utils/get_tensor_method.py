
def get_tensor_method() -> frozenset[Any]:
    disallowed_tensor_methods = {"__new__", "_make_wrapper_subclass", "_make_subclass"}
    s = set()
    for name in dir(torch.Tensor):
        method = getattr(torch.Tensor, name)
        if (
            isinstance(
                method,
                (
                    types.MethodDescriptorType,
                    types.WrapperDescriptorType,
                    types.BuiltinFunctionType,
                ),
            )
            and name not in disallowed_tensor_methods
        ):
            s.add(method)

    # mlazos: these are functions which we handle specially in TensorVariable
    s.add(torch.Tensor.__contains__)  # type: ignore[arg-type]
    s.add(torch.Tensor.register_hook)  # type: ignore[arg-type]
    return frozenset(s)

