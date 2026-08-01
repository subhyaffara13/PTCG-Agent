
def read_deps_cache(manager: BuildManager, graph: Graph) -> dict[str, FgDepMeta] | None:
    """Read and validate the fine-grained dependencies cache.

    See the write_deps_cache documentation for more information on
    the details of the cache.

    Returns None if the cache was invalid in some way.
    """
    deps_meta = _load_json_file(
        DEPS_META_FILE,
        manager,
        log_success="Deps meta ",
        log_error="Could not load fine-grained dependency metadata: ",
    )
    if deps_meta is None:
        return None
    meta_snapshot = deps_meta["snapshot"]
    # Take a snapshot of the source hashes from all the metas we found.
    # (Including the ones we rejected because they were out of date.)
    # We use this to verify that they match up with the proto_deps.
    current_meta_snapshot = {
        id: st.meta_source_hash for id, st in graph.items() if st.meta_source_hash is not None
    }

    common = set(meta_snapshot.keys()) & set(current_meta_snapshot.keys())
    if any(meta_snapshot[id] != current_meta_snapshot[id] for id in common):
        # TODO: invalidate also if options changed (like --strict-optional)?
        manager.log("Fine-grained dependencies cache inconsistent, ignoring")
        return None

    module_deps_metas = deps_meta["deps_meta"]
    assert isinstance(module_deps_metas, dict)
    if not manager.options.skip_cache_mtime_checks:
        for meta in module_deps_metas.values():
            try:
                matched = manager.getmtime(meta["path"]) == meta["mtime"]
            except FileNotFoundError:
                matched = False
            if not matched:
                manager.log(f"Invalid or missing fine-grained deps cache: {meta['path']}")
                return None

    return module_deps_metas

