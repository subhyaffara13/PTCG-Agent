
def _extract_single_node(code: str, module_name: str = "") -> nodes.NodeNG:
    """Call extract_node while making sure that only one value is returned."""
    ret = extract_node(code, module_name)
    if isinstance(ret, list):
        return ret[0]
    return ret

