
def get_parent_of_type(op: OpView | Operation, op_class: type[OpView]) -> OpView | None:
    """Return the closest enclosing parent operation of the given type.

    Walks the parent chain of *op* and returns the first ancestor that is an instance of *op_class*.
    Returns ``None`` if no matching parent is found.

    Args:
      op: The starting operation.
      op_class: The OpView subclass to search for (e.g. ``func.FuncOp``).

    """
    if not (isinstance(op_class, type) and issubclass(op_class, OpView)):
        raise TypeError(f"op_class must be an OpView subclass, got {op_class!r}")
    try:
        parent = op.parent
    except ValueError:
        return None  # No parent chain.
    while parent is not None:
        if isinstance(parent.opview, op_class):
            return parent.opview
        parent = parent.parent
    return None

