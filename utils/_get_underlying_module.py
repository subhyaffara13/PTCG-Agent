
def _get_underlying_module(
    module_or_method: torch.nn.Module | Callable[..., Any],
) -> torch.nn.Module:
    """Extract the underlying nn.Module from either a module or a bound method.

    Args:
        module_or_method: Either an nn.Module or a bound method of an nn.Module.

    Returns:
        The underlying nn.Module.

    Raises:
        TypeError: If module_or_method is neither an nn.Module nor a bound method.
    """
    if isinstance(module_or_method, torch.nn.Module):
        return module_or_method
    # Handle bound methods (e.g., module.method)
    if (
        mod_self := getattr(module_or_method, "__self__", None)
    ) is not None and isinstance(mod_self, torch.nn.Module):
        return mod_self
    raise TypeError(
        f"Expected nn.Module or bound method of nn.Module, got {type(module_or_method)}"
    )

