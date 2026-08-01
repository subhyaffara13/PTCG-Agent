
def erase_def_to_union_or_bound(tdef: TypeVarLikeType) -> Type:
    # TODO(PEP612): fix for ParamSpecType
    if isinstance(tdef, ParamSpecType):
        return AnyType(TypeOfAny.from_error)
    if isinstance(tdef, TypeVarType) and tdef.values:
        return make_simplified_union(tdef.values)
    else:
        return tdef.upper_bound

