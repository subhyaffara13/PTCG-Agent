
def _build_key_set(
    dsl_names: str | Iterable[str] | None,
    op_symbols: str | Iterable[str] | None,
    dispatch_keys: str | Iterable[str] | None,
) -> set[tuple[str, str]]:
    """
    Build a set of dictionary keys based on filter criteria.

    Args:
        dsl_names: DSL names to include in key set
        op_symbols: Operation symbols to include in key set
        dispatch_keys: Dispatch keys to include in key set

    Returns:
        set[tuple[str, str]]: Set of (op_symbol, dispatch_key) tuples
    """
    key_set: set[tuple[str, str]] = set()

    def _append_to_set(
        entries: str | Iterable[str] | None, graph_lib_dict: _MappingType
    ) -> None:
        """Helper to add matching keys from graph_lib_dict to key_set."""
        resolved_entries = _resolve_iterable(entries)

        for entry in resolved_entries:
            if entry in graph_lib_dict:
                for key in graph_lib_dict[entry]:
                    key_set.add(key)

    _append_to_set(dsl_names, _dsl_name_to_lib_graph)
    _append_to_set(op_symbols, _op_symbol_to_lib_graph)
    _append_to_set(dispatch_keys, _dispatch_key_to_lib_graph)

    return key_set

