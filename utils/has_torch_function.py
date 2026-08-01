
def has_torch_function(vt: VariableTracker) -> bool:
    # This emulates
    # https://github.com/pytorch/pytorch/blob/8d81806211bc3c0ee6c2ef235017bacf1d775a85/torch/csrc/utils/disable_torch_function.cpp#L315-L323
    from torch._dynamo.variables import UserDefinedObjectVariable
    from torch._dynamo.variables.torch_function import TensorWithTFOverrideVariable

    # Note on lazy vars: The value will either be realized or not throughout the course of execution
    # if the value has a torch function, it will eventually be realized so we can realize it here
    # if the value does not have a torch function, it may or may not be realized
    # if it is realized it will be used and guards will be installed properly
    # if it is not used, guards won't be installed, and it doesn't matter
    # if the value has a torch function or not, so we should *not* realize it.
    # NB: We technically know that if is_realized is False, LazyVariableTracker has the peek_value method
    # but mypy does not unfortunately
    if vt.is_realized() or (
        hasattr(vt, "peek_value") and hasattr(vt.peek_value(), "__torch_function__")
    ):
        func = None
        if isinstance(vt, TensorWithTFOverrideVariable):
            func = getattr(vt.class_type, "__torch_function__", None)

        elif isinstance(vt, UserDefinedObjectVariable):
            func = getattr(vt.value, "__torch_function__", None)

        return func not in (None, torch._C._disabled_torch_function_impl)

    return False

