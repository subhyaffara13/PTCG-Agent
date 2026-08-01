
def _is_keyword_only_sentinel(node: nodes.NodeNG) -> bool:
    """Return True if node is the KW_ONLY sentinel."""
    inferred = safe_infer(node)
    return (
        isinstance(inferred, bases.Instance)
        and inferred.qname() == "dataclasses._KW_ONLY_TYPE"
    )

