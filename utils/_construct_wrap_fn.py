
def _construct_wrap_fn(
    root_module: nn.Module,
    target_module_to_kwargs: dict[nn.Module, dict[str, Any]],
    fsdp_fn: Callable,
) -> Callable[[nn.Module], nn.Module | None]:
    """
    This constructs the "wrap" function to pass to :func:`_post_order_apply`
    based on ``target_module_to_kwargs``, which should be constructed from the
    wrapping policy.
    """

    def fn(module: nn.Module) -> nn.Module | None:
        # Explicitly avoid wrapping the root module since for FSDP, it is
        # handled by the caller
        if module in target_module_to_kwargs and module is not root_module:
            kwargs = target_module_to_kwargs[module]
            return fsdp_fn(module, **kwargs)
        return None

    return fn

