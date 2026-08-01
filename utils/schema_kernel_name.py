
def schema_kernel_name(func: FunctionSchema, dispatch_key: DispatchKey) -> str:
    if not func.is_out_fn():
        raise AssertionError("ufunc.kernel_name should only be invoked on out schemas")
    return f"ufunc_{func.name.name}_{dispatch_key}"

