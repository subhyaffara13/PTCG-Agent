
def _unwrap_type_type(tp: TypeType | UnionType) -> ProperType:
    """Extract the inner type from ``type[...]`` expression or a union thereof."""
    if isinstance(tp, TypeType):
        return tp.item
    return UnionType.make_union([cast(TypeType, get_proper_type(o)).item for o in tp.items])

