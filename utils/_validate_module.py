
def _validate_module(module: nn.Module) -> None:
    if not is_composable_with_replicate(module):
        raise RuntimeError(
            "Cannot apply `replicate()` on a Module already managed by `fully_shard`"
        )
    _validate_module_common(module, "replicate")


def _validate_module(module: nn.Module, func_name: str) -> None:
    """
    Validate that the module can be used with fully_shard or replicate.

    Raises ValueError if the module is a container that doesn't implement forward.
    """
    if (
        isinstance(module, (nn.ModuleList, nn.ModuleDict))
        and module.__class__.forward is nn.Module.forward
    ):
        raise ValueError(
            f"{func_name} does not support containers that do not implement forward: {module}"
        )

