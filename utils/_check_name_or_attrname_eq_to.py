
def _check_name_or_attrname_eq_to(
    node: nodes.Name | nodes.Attribute, check_with: str
) -> bool:
    """Utility function to check either a Name/Attribute node's name/attrname with a
    given string.
    """
    if isinstance(node, nodes.Name):
        return str(node.name) == check_with
    return str(node.attrname) == check_with

