
def custom_function_call_functionalize(
    interpreter: FuncTorchInterpreter,
    autograd_function: type[torch.autograd.Function],
    generate_vmap_rule: bool,
    *operands: Any,
) -> Any:
    raise RuntimeError("NYI: Functionalize rule for custom_function_call")

