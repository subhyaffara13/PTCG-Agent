
def str_formatting_in_f_string(node: nodes.JoinedStr) -> bool:
    """Determine whether the node represents an f-string with string formatting.

    For example: `f'Hello %s'`
    """
    # Check "%" presence first for performance.
    return any(
        "%" in val.value and any(x in val.value for x in MOST_COMMON_FORMATTING)
        for val in node.values
        if isinstance(val, nodes.Const)
    )

