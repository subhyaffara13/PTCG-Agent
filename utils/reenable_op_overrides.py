
def reenable_op_overrides(
    *,
    enable_dsl_names: str | list[str] | None = None,
    enable_op_symbols: str | list[str] | None = None,
    enable_dispatch_keys: str | list[str] | None = None,
) -> None:
    """
    Re-enable overrides by removing them from filter state and reregistering.

    Args:
        enable_dsl_names: DSL names to re-enable
        enable_op_symbols: Operation symbols to re-enable
        enable_dispatch_keys: Dispatch keys to re-enable

    Note:
        This function uses reverse filter state management (removing from
        filters to enable).
    """
    log.info(
        "Re-registering ops by dsl: %s, op_symbol: %s, dispatch_key: %s",
        enable_dsl_names,
        enable_op_symbols,
        enable_dispatch_keys,
    )

    # Update the filters - note `remove_keys=True` because
    # we are removing keys from the filters (vs. adding them)
    _filter_state.update(
        enable_dsl_names,
        enable_op_symbols,
        enable_dispatch_keys,
        remove_keys=True,
    )

    # Get the set of keys that need to be reprocessed
    key_set: set[tuple[str, str]] = _build_key_set(
        enable_dsl_names,
        enable_op_symbols,
        enable_dispatch_keys,
    )

    # Process each affected graph with updated filter state
    for key in key_set:
        op_symbol, dispatch_key = key

        if key in _graphs:
            # Note: We don't need to cleanup and recreate the library here
            # since we're just updating the registration with new filter state
            _register_overrides_from_graph(
                op_symbol, dispatch_key, _graphs[key], filter_state=_filter_state
            )

