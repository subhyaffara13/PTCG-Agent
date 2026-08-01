
def _load_cached_group_files(
    group_sources: list[BuildSource], result: BuildResult
) -> list[tuple[str, str]]:
    """Read the .c/.h paths recorded for this group on the previous run.

    All modules in a group share the same src_hashes map, so the first
    readable IR cache is sufficient. Returns paths paired with empty
    content so callers can distinguish "reuse on disk" from "newly
    generated".
    """
    for source in group_sources:
        state = result.graph.get(source.module)
        if state is None:
            continue
        try:
            ir_json = result.manager.metastore.read(get_state_ir_cache_name(state))
        except (FileNotFoundError, OSError):
            continue
        try:
            ir_data = json.loads(ir_json)
        except json.JSONDecodeError:
            continue
        return [(path, "") for path in ir_data.get("src_hashes", {})]
    return []

