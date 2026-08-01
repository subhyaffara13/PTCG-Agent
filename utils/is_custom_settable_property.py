
def is_custom_settable_property(defn: SymbolNode | None) -> bool:
    """Check if a node is a settable property with a non-trivial setter type.

    By non-trivial here we mean that it is known (i.e. definition was already type
    checked), it is not Any, and it is different from the property getter type.
    """
    if defn is None:
        return False
    if not is_settable_property(defn):
        return False
    first_item = defn.items[0]
    assert isinstance(first_item, Decorator)
    if not first_item.var.is_settable_property:
        return False
    var = first_item.var
    if var.type is None or var.setter_type is None or isinstance(var.type, PartialType):
        # The caller should defer in case of partial types or not ready variables.
        return False
    setter_type = var.setter_type.arg_types[1]
    if isinstance(get_proper_type(setter_type), AnyType):
        return False
    return not is_same_type(get_property_type(get_proper_type(var.type)), setter_type)

