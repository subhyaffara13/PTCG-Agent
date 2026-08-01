
def multi_device_op_default(
    fake_mode: FakeTensorMode, func: OpOverload, *args: Any, **kwargs: Any
) -> FakeTensor:
    return run_and_return_new_tensor_of_input_device(fake_mode, func, args, kwargs)

