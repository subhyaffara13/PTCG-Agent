import time

def process_stale_scc(graph: Graph, ascc: SCC, manager: BuildManager) -> None:
    """Process the modules in one SCC from source code."""
    # First verify if all transitive dependencies are loaded in the current process.
    t0 = time.time()
    maybe_load_deps(graph, ascc, manager)
    t1 = time.time()
    # Process the SCC in stable order.
    scc = order_ascc_ex(graph, ascc)

    t2 = time.time()
    stale = scc
    # Parse before verify_dependencies so that inline config comments
    # (e.g. "# mypy: disable-error-code") are applied to options.
    manager.parse_all([graph[id] for id in stale], post_parse=False)
    for id in stale:
        # Re-generate import errors in case this module was loaded from the cache.
        if graph[id].meta:
            graph[id].verify_dependencies(suppressed_only=True)
    if "typing" in scc:
        # For historical reasons we need to manually add typing aliases
        # for built-in generic collections, see docstring of
        # SemanticAnalyzerPass2.add_builtin_aliases for details.
        typing_mod = graph["typing"].tree
        assert typing_mod, "The typing module was not parsed"
    mypy.semanal_main.semantic_analysis_for_scc(graph, scc, manager.errors)

    t3 = time.time()
    # Track what modules aren't yet done, so we can finish them as soon
    # as possible, saving memory.
    unfinished_modules = set(stale)
    for id in stale:
        graph[id].type_check_first_pass()
        if not graph[id].type_checker().deferred_nodes:
            unfinished_modules.discard(id)
            graph[id].detect_possibly_undefined_vars()
            graph[id].finish_passes()

    while unfinished_modules:
        for id in stale:
            if id not in unfinished_modules:
                continue
            if not graph[id].type_check_second_pass():
                unfinished_modules.discard(id)
                graph[id].detect_possibly_undefined_vars()
                graph[id].finish_passes()
    for id in stale:
        graph[id].generate_unused_ignore_notes()
        graph[id].generate_ignore_without_code_notes()

    t4 = time.time()
    # Flush errors, and write cache in two phases: first data files, then meta files.
    # The two-phase structure is needed because meta.dep_hashes references interface_hash
    # values from other modules in the SCC, which are updated by write_cache().
    meta_tuples = {}
    errors_by_id = {}
    for id in stale:
        if graph[id].xpath not in manager.errors.ignored_files:
            errors = manager.errors.file_messages(graph[id].xpath)
            formatted = manager.errors.format_messages(
                graph[id].xpath, errors, formatter=manager.error_formatter
            )
            manager.flush_errors(manager.errors.simplify_path(graph[id].xpath), formatted, False)
            errors_by_id[id] = errors
        meta_tuple = graph[id].write_cache()
        meta_tuples[id] = meta_tuple
        # Commit data file write immediately to avoid holding shard locks across modules.
        if meta_tuple is not None:
            manager.commit_module(meta_tuple[1])
    for id in stale:
        meta_tuple = meta_tuples[id]
        if meta_tuple is None:
            continue
        meta, meta_file = meta_tuple
        state = graph[id]
        # Indirect dependencies are stored as part of CacheMetaEx below.
        meta.dep_hashes = [
            graph[dep].interface_hash
            for dep in graph[id].dependencies
            if state.priorities.get(dep) != PRI_INDIRECT
        ]
        write_cache_meta(meta, manager, meta_file)
        indirect = [dep for dep in state.dependencies if state.priorities.get(dep) == PRI_INDIRECT]
        meta_ex = CacheMetaEx(
            dependencies=indirect,
            suppressed=[
                dep for dep in state.suppressed if state.priorities.get(dep) == PRI_INDIRECT
            ],
            dep_hashes=[graph[dep].interface_hash for dep in indirect],
            error_lines=errors_by_id.get(id, []),
        )
        write_cache_meta_ex(meta_file, meta_ex, manager)
        manager.commit_module(meta_file)
    manager.done_sccs.add(ascc.id)
    manager.add_stats(
        load_missing_time=t1 - t0,
        order_scc_time=t2 - t1,
        semanal_time=t3 - t2,
        type_check_time=t4 - t3,
        flush_and_cache_time=time.time() - t4,
    )

