
def _get_attrs_init_type(typ: Instance) -> CallableType | None:
    """
    If `typ` refers to an attrs class, get the type of its initializer method.
    """
    magic_attr = typ.type.get(MAGIC_ATTR_NAME)
    if magic_attr is None or not magic_attr.plugin_generated:
        return None
    init_method = typ.type.get_method("__init__") or typ.type.get_method(ATTRS_INIT_NAME)
    if not isinstance(init_method, FuncDef) or not isinstance(init_method.type, CallableType):
        return None
    return init_method.type

