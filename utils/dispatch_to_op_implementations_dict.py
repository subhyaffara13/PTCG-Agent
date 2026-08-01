
def dispatch_to_op_implementations_dict(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> Any:
    return op_implementations_dict[func](fake_mode, func, *args, **kwargs)

