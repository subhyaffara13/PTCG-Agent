
def _get_managed_modules(
    root_modules: tuple[nn.Module, ...],
    ignored_params: set[nn.Parameter] | None = None,
    is_composable_fn: "Callable[[nn.Module], bool] | None" = None,
    get_state_fn: "Callable[[nn.Module], Any] | None" = None,
) -> list[nn.Module]:
    """
    Get the list of managed modules for FSDP/replicate.

    Args:
        root_modules: The root modules to start the search from.
        ignored_params: Parameters to ignore.
        is_composable_fn: Callable to check if a module is composable.
            Defaults to ``_is_composable_with_fsdp``.
        get_state_fn: Callable to get the state of a module.
            Defaults to ``_get_module_fsdp_state``.
    """
    if is_composable_fn is None:
        is_composable_fn = _is_composable_with_fsdp
    if get_state_fn is None:
        get_state_fn = _get_module_fsdp_state

    modules: list[nn.Module] = []
    root_modules_set = set(root_modules)
    # Track visisted modules to avoid visiting shared modules multiple times
    visited_modules: set[nn.Module] = set()

    def dfs(module: nn.Module) -> None:
        """
        Runs a DFS to collect managed modules, not recursing into modules with
        a non-composable API or ``fully_shard`` already applied.
        """
        if not is_composable_fn(module):
            return
        elif module not in root_modules_set and get_state_fn(module) is not None:
            return  # nested `fully_shard` module
        visited_modules.add(module)
        for submodule in module.children():
            if submodule not in visited_modules:
                dfs(submodule)
        modules.append(module)

    for root_module in root_modules:
        dfs(root_module)

    if ignored_params is None:
        return modules

    adjusted_modules = _adjust_managed_modules(modules, ignored_params)
    return adjusted_modules

