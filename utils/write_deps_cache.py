
def write_deps_cache(
    rdeps: dict[str, dict[str, set[str]]], manager: BuildManager, graph: Graph
) -> None:
    """Write cache files for fine-grained dependencies.

    Serialize fine-grained dependencies map for fine-grained mode.

    Dependencies on some module 'm' is stored in the dependency cache
    file m.deps.json.  This entails some spooky action at a distance:
    if module 'n' depends on 'm', that produces entries in m.deps.json.
    When there is a dependency on a module that does not exist in the
    build, it is stored with its first existing parent module. If no
    such module exists, it is stored with the fake module FAKE_ROOT_MODULE.

    This means that the validity of the fine-grained dependency caches
    are a global property, so we store validity checking information for
    fine-grained dependencies in a global cache file:
     * We take a snapshot of current sources to later check consistency
       between the fine-grained dependency cache and module cache metadata
     * We store the mtime of all the dependency files to verify they
       haven't changed
    """
    metastore = manager.metastore

    error = False

    fg_deps_meta = manager.fg_deps_meta.copy()

    for id in rdeps:
        if id != FAKE_ROOT_MODULE:
            _, _, deps_json = get_cache_names(id, graph[id].xpath, manager.options)
        else:
            deps_json = DEPS_ROOT_FILE
        assert deps_json
        manager.log("Writing deps cache", deps_json)
        if not manager.metastore.write(deps_json, deps_to_json(rdeps[id])):
            manager.log(f"Error writing fine-grained deps JSON file {deps_json}")
            error = True
        else:
            fg_deps_meta[id] = {"path": deps_json, "mtime": manager.getmtime(deps_json)}

    meta_snapshot: dict[str, str] = {}
    for id, st in graph.items():
        # If we didn't parse a file (so it doesn't have a
        # source_hash), then it must be a module with a fresh cache,
        # so use the hash from that.
        if st.source_hash:
            hash = st.source_hash
        else:
            if st.meta:
                hash = st.meta.hash
            else:
                hash = ""
        meta_snapshot[id] = hash

    meta = {"snapshot": meta_snapshot, "deps_meta": fg_deps_meta}

    if not metastore.write(DEPS_META_FILE, json_dumps(meta)):
        manager.log(f"Error writing fine-grained deps meta JSON file {DEPS_META_FILE}")
        error = True

    if error:
        manager.errors.set_file(_cache_dir_prefix(manager.options), None, manager.options)
        manager.error(None, "Error writing fine-grained dependencies cache", blocker=True)

