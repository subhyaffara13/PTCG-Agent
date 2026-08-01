
def activate_flash_attention_impl(
    impl: str | _FlashAttentionImpl,
) -> None:
    """
    Activate into the dispatcher a previously registered flash attention impl.

    .. note::
        Backend providers should NOT automatically activate their implementation
        on import. Users should explicitly opt-in by calling this function or via
        environment variables to ensure multiple provider libraries can coexist.

    Args:
        impl: Implementation identifier to activate. See
            :func:`~torch.nn.attention.list_flash_attention_impls` for available
            implementations.
            If the backend's :func:`register_flash_attention_impl` callable
            returns a :class:`FlashAttentionHandle`, the registry keeps that
            handle alive for the lifetime of the process (until explicit
            uninstall support exists).

    Example:
        >>> activate_flash_attention_impl("FA4")  # doctest: +SKIP
    """
    global _FLASH_ATTENTION_ACTIVE, _FLASH_ATTENTION_IMPLS

    restore_flash_attention_impl(
        _raise_warn=False
    )  # first restore any prev overrides (if any) to default

    register_fn = _FLASH_ATTENTION_IMPLS.get(impl)
    if register_fn is None:
        raise ValueError(
            f"Unknown flash attention impl '{impl}'. "
            f"Available implementations: {list_flash_attention_impls()}"
        )

    handle = register_fn()
    if handle is not None:
        _FLASH_ATTENTION_ACTIVE = (impl, handle)

