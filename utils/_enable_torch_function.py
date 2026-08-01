
def _enable_torch_function():
    old_state = torch._C._get_torch_function_state()
    try:
        torch._C._set_torch_function_state(torch._C._TorchFunctionState.ENABLED)
        yield
    finally:
        torch._C._set_torch_function_state(old_state)

