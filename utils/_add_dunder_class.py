
def _add_dunder_class(func, parent: nodes.NodeNG, member) -> None:
    """Add a __class__ member to the given func node, if we can determine it."""
    python_cls = member.__class__
    cls_name = getattr(python_cls, "__name__", None)
    if not cls_name:
        return
    cls_bases = [ancestor.__name__ for ancestor in python_cls.__bases__]
    doc = python_cls.__doc__ if isinstance(python_cls.__doc__, str) else None
    ast_klass = build_class(cls_name, parent, cls_bases, doc)
    func.instance_attrs["__class__"] = [ast_klass]

