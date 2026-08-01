
def _update_registration_maps(
    dsl_name: str,
    op_symbol: str,
    dispatch_key: str,
    key: tuple[str, str],
) -> None:
    """
    Update the registration mapping dictionaries.

    Args:
        dsl_name: The DSL name
        op_symbol: The operation symbol
        dispatch_key: The dispatch key
        key: The dictionary key tuple
    """
    global _dsl_name_to_lib_graph
    global _op_symbol_to_lib_graph
    global _dispatch_key_to_lib_graph

    def _get_new_entry_or_append(
        registration: dict[str, list[tuple[str, str]]],
        symbol: str,
        key: tuple[str, str],
    ) -> None:
        """Helper to add key to registration list or create new entry."""
        entry_list = registration.get(symbol)

        if entry_list is None:
            entry_list = [key]
            registration[symbol] = entry_list
        else:
            entry_list.append(key)

    _get_new_entry_or_append(_dsl_name_to_lib_graph, dsl_name, key)
    _get_new_entry_or_append(_op_symbol_to_lib_graph, op_symbol, key)
    _get_new_entry_or_append(_dispatch_key_to_lib_graph, dispatch_key, key)

