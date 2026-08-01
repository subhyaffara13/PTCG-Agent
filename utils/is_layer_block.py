
def is_layer_block(node):
    """
    Checks whether a node represents a layer block with submodules.

    Args:
        node (`dict`): A node from the call tree.

    Returns:
        `bool`: Whether the node is a layer block.
    """
    match = LAYER_SUFFIX_RE.match(node.get("module_path", ""))
    if not match or not node.get("children"):
        return False
    number = match.group(2)
    return any(f".{number}." in child.get("module_path", "") for child in node["children"])

