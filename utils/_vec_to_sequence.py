
def _vec_to_sequence(
    builder: LowLevelIRBuilder, vec: Value, line: int, method: str, result_type: RType
) -> Value | None:
    vec_type = vec.type
    assert isinstance(vec_type, RVec)
    item_type = vec_type.item_type
    api_name = vec_api_by_item_type.get(item_type)
    if api_name is not None:
        name = f"{api_name}.{method}"
    elif supports_vec_to_sequence(vec_type):
        name = f"VecTApi.{method}"
    else:
        return None
    return builder.add(
        CallC(
            name,
            [vec],
            result_type,
            steals=[True],
            is_borrowed=False,
            error_kind=ERR_MAGIC,
            line=line,
        )
    )

