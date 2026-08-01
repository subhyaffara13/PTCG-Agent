
def const_factory(value: Any) -> ConstFactoryResult:
    """Return an astroid node for a python value."""
    # NOTE: avoid accessing any attributes of value until it is known that value
    # is of a const type, to avoid possibly triggering code for a live object.
    # Accesses include value.__class__ and isinstance(value, ...), but not type(value).
    # See: https://github.com/pylint-dev/astroid/issues/2686
    value_type = type(value)
    assert not issubclass(value_type, NodeNG)

    # This only handles instances of the CONST types. Any
    # subclasses get inferred as EmptyNode.
    # TODO: See if we should revisit these with the normal builder.
    if value_type not in CONST_CLS:
        node = EmptyNode()
        node.object = value
        return node

    instance: List | Set | Tuple | Dict
    initializer_cls = CONST_CLS[value_type]
    if issubclass(initializer_cls, (List, Set, Tuple)):
        instance = initializer_cls(
            lineno=None,
            col_offset=None,
            parent=SYNTHETIC_ROOT,
            end_lineno=None,
            end_col_offset=None,
        )
        instance.postinit(_create_basic_elements(value, instance))
        return instance
    if issubclass(initializer_cls, Dict):
        instance = initializer_cls(
            lineno=None,
            col_offset=None,
            parent=SYNTHETIC_ROOT,
            end_lineno=None,
            end_col_offset=None,
        )
        instance.postinit(_create_dict_items(value, instance))
        return instance
    return Const(value)

