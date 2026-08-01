
def builtin_item_type(tp: Type) -> Type | None:
    """Get the item type of a builtin container.

    If 'tp' is not one of the built containers (these includes NamedTuple and TypedDict)
    or if the container is not parameterized (like List or List[Any])
    return None. This function is used to narrow optional types in situations like this:

        x: Optional[int]
        if x in (1, 2, 3):
            x + 42  # OK

    Note: this is only OK for built-in containers, where we know the behavior
    of __contains__.
    """
    tp = get_proper_type(tp)

    if isinstance(tp, Instance):
        if tp.type.fullname in [
            "builtins.list",
            "builtins.tuple",
            "builtins.dict",
            "builtins.frozendict",
            "builtins.set",
            "builtins.frozenset",
            "_collections_abc.dict_keys",
            "typing.KeysView",
        ]:
            if not tp.args:
                # TODO: fix tuple in lib-stub/builtins.pyi (it should be generic).
                return None
            if not isinstance(get_proper_type(tp.args[0]), AnyType):
                return tp.args[0]
    elif isinstance(tp, TupleType):
        normalized_items = []
        for it in tp.items:
            # This use case is probably rare, but not handling unpacks here can cause crashes.
            if isinstance(it, UnpackType):
                unpacked = get_proper_type(it.type)
                if isinstance(unpacked, TypeVarTupleType):
                    unpacked = get_proper_type(unpacked.upper_bound)
                assert (
                    isinstance(unpacked, Instance) and unpacked.type.fullname == "builtins.tuple"
                )
                normalized_items.append(unpacked.args[0])
            else:
                normalized_items.append(it)
        if all(not isinstance(it, AnyType) for it in get_proper_types(normalized_items)):
            return make_simplified_union(normalized_items)  # this type is not externally visible
    elif isinstance(tp, TypedDictType):
        # TypedDict always has non-optional string keys. Find the key type from the Mapping
        # base class.
        for base in tp.fallback.type.mro:
            if base.fullname == "typing.Mapping":
                return map_instance_to_supertype(tp.fallback, base).args[0]
        assert False, "No Mapping base class found for TypedDict fallback"
    return None

