
def anchorsValidator(value: Any, identifiers: Optional[set[str]] = None) -> bool:
    """
    Version 3+.
    """
    if not isinstance(value, list):
        return False
    if identifiers is None:
        identifiers = set()
    for anchor in value:
        if not anchorValidator(anchor):
            return False
        identifier = anchor.get("identifier")
        if identifier is not None:
            if identifier in identifiers:
                return False
            identifiers.add(identifier)
    return True

