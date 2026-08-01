
def _is_raising(body: list[nodes.NodeNG]) -> bool:
    """Return whether the given statement node raises an exception."""
    return any(isinstance(node, nodes.Raise) for node in body)

