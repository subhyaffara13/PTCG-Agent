
def parse_node_kind(kind: str) -> tuple[str, str]:
    """Parse node kind into domain and Op name."""
    if "::" not in kind:
        raise ValueError(f"Node kind: {kind} is invalid. '::' is not in node kind.")
    domain, opname = kind.split("::", 1)
    if "::" in opname:
        raise ValueError(f"Node kind: {kind} is invalid. '::' should only appear once.")
    return domain, opname

