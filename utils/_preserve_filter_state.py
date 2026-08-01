
def _preserve_filter_state():
    """Context manager to save and restore registry filter state."""
    filter_state = _get_filter_state()

    # Save original state
    original_state = (
        set(filter_state._dsl_names),
        set(filter_state._op_symbols),
        set(filter_state._dispatch_keys),
    )

    try:
        yield filter_state
    finally:
        # Restore original state
        filter_state._dsl_names.clear()
        filter_state._op_symbols.clear()
        filter_state._dispatch_keys.clear()

        filter_state._dsl_names.update(original_state[0])
        filter_state._op_symbols.update(original_state[1])
        filter_state._dispatch_keys.update(original_state[2])

