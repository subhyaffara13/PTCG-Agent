
def split_import_group_to_python_and_native(
    builder: IRBuilder, group: list[Import]
) -> list[tuple[list[tuple[str, str | None, int]], bool]]:
    """Split imports into consecutive runs of native same-group and non-native imports."""
    flat_list = []
    for imp in group:
        for mod_id, as_name in imp.ids:
            flat_list.append(
                (
                    mod_id,
                    as_name,
                    imp.line,
                    builder.is_native_module(mod_id) and builder.is_same_group_module(mod_id),
                )
            )
    result = []
    i = 0
    while i < len(flat_list):
        i0 = i
        is_native = flat_list[i][3]
        i += 1
        while i < len(flat_list) and flat_list[i][3] == is_native:
            i += 1
        result.append(([t[:3] for t in flat_list[i0:i]], is_native))
    return result

