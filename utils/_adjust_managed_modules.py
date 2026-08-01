
def _adjust_managed_modules(
    modules: list[nn.Module], ignored_params: set[nn.Parameter]
) -> list[nn.Module]:
    """
    Adjust the given list of managed modules by removing those with all parameters ignored.
    """
    ignore_decision: dict[nn.Module, bool] = {}
    new_modules = []
    for module in modules:
        ignored = _ignore_module(module, ignored_params, ignore_decision)
        if not ignored:
            new_modules.append(module)
    return new_modules

