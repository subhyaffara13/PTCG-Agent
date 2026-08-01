
def get_fslocation_from_item(node: Node) -> tuple[str | Path, int | None]:
    """Try to extract the actual location from a node, depending on available attributes:

    * "location": a pair (path, lineno)
    * "obj": a Python object that the node wraps.
    * "path": just a path

    :rtype: A tuple of (str|Path, int) with filename and 0-based line number.
    """
    # See Item.location.
    location: tuple[str, int | None, str] | None = getattr(node, "location", None)
    if location is not None:
        return location[:2]
    obj = getattr(node, "obj", None)
    if obj is not None:
        return getfslineno(obj)
    return getattr(node, "path", "unknown location"), -1

