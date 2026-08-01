
def register_op_override(
    lib_symbol: str,
    op_symbol: str,
    dispatch_key: str,
    impl: _OpFn,
    *,
    allow_multiple_override: bool = False,
    unconditional_override: bool = False,
) -> None:
    """
    See torch/_native/registry.py for the underlying implementation
    and arguments. This is a thin, DSL-checking wrapper over
    _register_op_override_impl
    """
    available, version = _check_runtime_available()
    if (not available) or check_native_jit_disabled():
        return

    if not _version_is_ok():
        return

    _register_op_override_impl(
        _CUTEDSL_DSL_NAME,
        lib_symbol,
        op_symbol,
        dispatch_key,
        impl,
        allow_multiple_override=allow_multiple_override,
        unconditional_override=unconditional_override,
    )


def register_op_override(
    backend: str,
    lib_symbol: str,
    op_symbol: str,
    dispatch_key: str,
    impl: _OpOverrideFn | _OpReplaceFn,
    *,
    allow_multiple_override: bool = False,
    unconditional_override: bool = False,
) -> None:
    """
    Register a passed override function to the dispatcher.

    Actually a graph-building operation; real registration happens later.

    Args:
        backend: The backend name (DSL name)
        lib_symbol: Library you're overriding symbols in (must be "aten")
        op_symbol: Name of the operation you're overriding
        dispatch_key: Dispatch key to override
        impl: Implementation function for the override
        allow_multiple_override: Allow overriding an existing override
        unconditional_override: Implementation doesn't have a fallback and
            doesn't require torch.DispatchKeySet as the first argument

    Raises:
        ValueError: If lib_symbol is not "aten"
    """
    if lib_symbol != "aten":
        raise ValueError(f'Unsupported lib_symbol (must be "aten", got: "{lib_symbol}"')

    key = (op_symbol, dispatch_key)

    global _graphs
    op_graph = _graphs.get(key, [])

    op_graph.append(
        _OverrideNode(
            dsl_name=backend,
            op_symbol=op_symbol,
            dispatch_key=dispatch_key,
            override_fn=impl,
            unconditional_override=unconditional_override,
        )
    )
    _graphs[key] = op_graph
    # Build additional maps helpful for de-registration
    _update_registration_maps(backend, op_symbol, dispatch_key, key=key)


def register_op_override(
    lib_symbol: str,
    op_symbol: str,
    dispatch_key: str,
    impl: _OpFn,
    *,
    allow_multiple_override: bool = False,
    unconditional_override: bool = False,
) -> None:
    """
    See torch/_native/registry.py for the underlying implementation
    and arguments. This is a thin, DSL-checking wrapper over
    _register_op_override_impl
    """
    available, version = _check_runtime_available()
    if (not available) or check_native_jit_disabled():
        return

    if not _version_is_sufficient():
        return

    _register_op_override_impl(
        _TRITON_DSL_NAME,
        lib_symbol,
        op_symbol,
        dispatch_key,
        impl,
        allow_multiple_override=allow_multiple_override,
        unconditional_override=unconditional_override,
    )

