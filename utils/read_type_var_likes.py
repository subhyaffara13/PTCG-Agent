
def read_type_var_likes(data: ReadBuffer) -> list[TypeVarLikeType]:
    """Specialized version of read_type_list() for lists of type variables."""
    assert read_tag(data) == LIST_GEN
    ret: list[TypeVarLikeType] = []
    for _ in range(read_int_bare(data)):
        tag = read_tag(data)
        if tag == TYPE_VAR_TYPE:
            ret.append(TypeVarType.read(data))
        elif tag == PARAM_SPEC_TYPE:
            ret.append(ParamSpecType.read(data))
        elif tag == TYPE_VAR_TUPLE_TYPE:
            ret.append(TypeVarTupleType.read(data))
        else:
            assert False, f"Invalid type tag for TypeVarLikeType {tag}"
    return ret

