
def _materialize_with_param_init_fn(
    root_module: nn.Module,
    param_init_fn: Callable[[nn.Module], None],
    ignored_modules: set[nn.Module],
) -> None:
    if not callable(param_init_fn):
        raise ValueError(
            f"Expected {param_init_fn} to be callable but got {type(param_init_fn)}"
        )
    modules_to_materialize = _get_modules_to_materialize(root_module, ignored_modules)
    for module in modules_to_materialize:
        param_init_fn(module)

