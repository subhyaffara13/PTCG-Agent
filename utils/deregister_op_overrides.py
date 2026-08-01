
def deregister_op_overrides() -> None:
    """
    Deregister all ops through cuteDSL
    """
    _deregister_op_overrides_impl(disable_dsl_names=_CUTEDSL_DSL_NAME)


def deregister_op_overrides(
    *,
    disable_dsl_names: str | list[str] | None = None,
    disable_op_symbols: str | list[str] | None = None,
    disable_dispatch_keys: str | list[str] | None = None,
) -> None:
    """
    De-register overrides by updating filter state and reregistering graphs.

    Args:
        disable_dsl_names: DSL names to disable
        disable_op_symbols: Operation symbols to disable
        disable_dispatch_keys: Dispatch keys to disable

    Note:
        This function uses filter state management to selectively disable
        operations.
    """
    log.info(
        "De-registering ops by dsl: %s, op_symbol: %s, dispatch_key: %s",
        disable_dsl_names,
        disable_op_symbols,
        disable_dispatch_keys,
    )

    # Update filter state to disable specified entries
    _filter_state.update(disable_dsl_names, disable_op_symbols, disable_dispatch_keys)

    # Get the set of keys that need to be reprocessed
    key_set: set[tuple[str, str]] = _filter_state.build_disable_key_set()

    # Process each affected graph with filter state
    for key in key_set:
        op_symbol, dispatch_key = key

        if key in _graphs:
            _cleanup_and_reregister_graph(
                op_symbol,
                dispatch_key,
                _graphs[key],
                filter_state=_filter_state,
            )


def deregister_op_overrides() -> None:
    """
    Deregister all ops through triton
    """
    _deregister_op_overrides_impl(disable_dsl_names=_TRITON_DSL_NAME)

