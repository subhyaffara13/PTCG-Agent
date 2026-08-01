
def write_undocumented_ref_info(
    state: State, metastore: MetadataStore, options: Options, type_map: dict[Expression, Type]
) -> None:
    # This exports some dependency information in a rather ad-hoc fashion, which
    # can be helpful for some tools. This is all highly experimental and could be
    # removed at any time.

    from mypy.refinfo import get_undocumented_ref_info_json

    if not state.tree:
        # We need a full AST for this.
        return

    _, data_file, _ = get_cache_names(state.id, state.xpath, options)
    ref_info_file = ".".join(data_file.split(".")[:-2]) + ".refs.json"
    assert not ref_info_file.startswith(".")

    deps_json = get_undocumented_ref_info_json(state.tree, type_map)
    metastore.write(ref_info_file, json_dumps(deps_json))

