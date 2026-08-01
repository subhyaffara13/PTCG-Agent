
def make_eager_backend_with_torch_function_mode(
    mode: torch.overrides.TorchFunctionMode,
) -> Callable[..., Any]:
    return make_eager_backend_with_torch_function_modes([mode])

