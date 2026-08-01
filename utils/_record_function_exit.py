
def _record_function_exit(
    fake_mode: FakeTensorMode, func: OpOverload, handle: Any
) -> None:
    # Exit doesn't return anything and doesn't need to do anything for fake tensors
    # Just return None (the actual return type is void)
    pass

