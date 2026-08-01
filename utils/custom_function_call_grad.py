
def custom_function_call_grad(
    interpreter: FuncTorchInterpreter,
    autograd_function: type[torch.autograd.Function],
    *operands: Any,
) -> Any:
    Generated = generate_single_level_function(interpreter, autograd_function)
    with enable_single_level_autograd_function():
        # pyrefly: ignore [missing-attribute]
        flat_out = Generated.apply(*operands)
    return flat_out

