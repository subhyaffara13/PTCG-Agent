
def covers_at_runtime(item: Type, supertype: Type) -> bool:
    """Will isinstance(item, supertype) always return True at runtime?"""
    item = get_proper_type(item)
    supertype = get_proper_type(supertype)

    # Since runtime type checks will ignore type arguments, erase the types.
    if not (isinstance(supertype, FunctionLike) and supertype.is_type_obj()):
        supertype = erase_type(supertype)
    if is_proper_subtype(
        erase_type(item), supertype, ignore_promotions=True, erase_instances=True
    ):
        return True
    if isinstance(supertype, Instance):
        if supertype.type.is_protocol:
            # TODO: Implement more robust support for runtime isinstance() checks, see issue #3827.
            if is_proper_subtype(item, supertype, ignore_promotions=True):
                return True
        if isinstance(item, TypedDictType):
            # Special case useful for selecting TypedDicts from unions using isinstance(x, dict).
            if supertype.type.fullname == "builtins.dict":
                return True
        elif isinstance(item, TypeVarType):
            if is_proper_subtype(item.upper_bound, supertype, ignore_promotions=True):
                return True
        elif isinstance(item, Instance) and supertype.type.fullname == "builtins.int":
            # "int" covers all native int types
            if item.type.fullname in MYPYC_NATIVE_INT_NAMES:
                return True
    # TODO: Add more special cases.
    return False

