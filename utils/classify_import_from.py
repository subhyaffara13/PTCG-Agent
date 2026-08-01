
def classify_import_from(
    builder: IRBuilder,
    module_id: str,
    names: list[str],
    as_names: list[str],
    parent_is_native: bool,
) -> list[ImportFromBucket]:
    """Classify each imported name and group consecutive same-kind names into buckets."""
    flat_list = []
    for name, as_name in zip(names, as_names):
        submodule_id = f"{module_id}.{name}"
        if builder.is_native_module(submodule_id) and builder.is_same_group_module(submodule_id):
            kind = IMPORT_NATIVE_SUBMODULE
        elif parent_is_native and submodule_id not in builder.graph:
            kind = IMPORT_NATIVE_ATTR
        else:
            kind = IMPORT_NON_NATIVE
        flat_list.append((kind, name, as_name))
    return group_consecutive(flat_list)

