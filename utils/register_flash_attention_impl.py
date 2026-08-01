
def register_flash_attention_impl(
    impl: str | _FlashAttentionImpl,
    *,
    register_fn: _RegisterFn,
) -> None:
    """
    Register the callable that activates a flash attention impl.

    .. note::
        This function is intended for SDPA backend providers to register their
        implementations. End users should use :func:`activate_flash_attention_impl`
        to activate a registered implementation.

    Args:
        impl: Implementation identifier (e.g., ``"FA4"``).
        register_fn: Callable that performs the actual dispatcher registration.
            This function will be invoked by :func:`activate_flash_attention_impl`
            and should register custom kernels with the PyTorch dispatcher.
            It may optionally return a handle implementing
            :class:`FlashAttentionHandle` to keep any necessary state alive.

    Example:
        >>> def my_impl_register(module_path: str = "my_flash_impl"):
        ...     # Register custom kernels with torch dispatcher
        ...     pass  # doctest: +SKIP
        >>> register_flash_attention_impl(
        ...     "MyImpl", register_fn=my_impl_register
        ... )  # doctest: +SKIP
    """
    global _FLASH_ATTENTION_IMPLS
    _FLASH_ATTENTION_IMPLS[impl] = register_fn

