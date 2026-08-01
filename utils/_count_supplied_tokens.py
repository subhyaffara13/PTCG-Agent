
def _count_supplied_tokens(args: list[nodes.NodeNG]) -> int:
    """Counts the number of tokens in an args list.

    The Python log functions allow for special keyword arguments: func,
    exc_info and extra. To handle these cases correctly, we only count
    arguments that aren't keywords.

    Args:
      args: AST nodes that are arguments for a log format string.

    Returns:
      Number of AST nodes that aren't keywords.
    """
    return sum(1 for arg in args if not isinstance(arg, nodes.Keyword))

