
def _is_attribute_property(name: str, klass: nodes.ClassDef) -> bool:
    """Check if the given attribute *name* is a property in the given *klass*.

    It will look for `property` calls or for functions
    with the given name, decorated by `property` or `property`
    subclasses.
    Returns ``True`` if the name is a property in the given klass,
    ``False`` otherwise.
    """
    try:
        attributes = klass.getattr(name)
    except astroid.NotFoundError:
        return False
    property_name = "builtins.property"
    for attr in attributes:
        if isinstance(attr, util.UninferableBase):
            continue
        try:
            inferred = next(attr.infer())
        except astroid.InferenceError:
            continue
        if isinstance(inferred, nodes.FunctionDef) and decorated_with_property(
            inferred
        ):
            return True
        if inferred.pytype() == property_name:
            return True
    return False

