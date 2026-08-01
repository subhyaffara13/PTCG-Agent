
def has_guarding_hint(a: Scalar) -> bool:
    """
    Check if a symbolic value has a hint available for guarding.

    Returns True if the value is concrete or if the symbolic node has a hint,
    False otherwise.
    """
    if isinstance(a, SymTypes):
        return a.node.has_hint()
    return True

