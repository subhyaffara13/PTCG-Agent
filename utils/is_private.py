
def is_private(node_name: str) -> bool:
    """Check if node is private to class definition."""
    return node_name.startswith("__") and not node_name.endswith("__")

