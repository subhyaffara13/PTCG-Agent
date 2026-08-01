
def get_dsl_operations(dsl_name: str) -> list[str]:
    """Get list of operations registered by a specific DSL.

    Args:
        dsl_name: Name of the DSL to query.

    Returns:
        Sorted list of operation names registered by the DSL.
    """
    operations = set()
    for (op_symbol, _), nodes in _graphs.items():
        for node in nodes:
            if node.dsl_name == dsl_name:
                operations.add(op_symbol)
                break
    return sorted(operations)

