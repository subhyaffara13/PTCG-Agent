
def _get_scope_name(scoped_name: str) -> tuple[str, str]:
    """Get the scope and name of a node.

    Examples::
        >>> _get_scope_name('')
        ('', '')
        >>> _get_scope_name('true_graph')
        ('', 'true_graph')
        >>> _get_scope_name('true_graph.false_graph')
        ('true_graph', 'false_graph')
        >>> _get_scope_name('true_graph.false_graph.some_graph')
        ('true_graph.false_graph', 'some_graph')

    Args:
        scoped_name: The scoped name of the node.

    Returns:
        (scope, name)
    """
    if "." in scoped_name:
        scope, name = scoped_name.rsplit(".", 1)
    else:
        scope, name = "", scoped_name
    return scope, name

