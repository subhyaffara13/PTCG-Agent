
def legacy_get_enum(
    size_average: bool | None,
    reduce: bool | None,
    emit_warning: bool = True,
) -> int:
    return get_enum(legacy_get_string(size_average, reduce, emit_warning))

