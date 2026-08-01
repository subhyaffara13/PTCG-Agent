
def process_stale_scc_interface(
    graph: Graph, ascc: SCC, manager: BuildManager, from_cache: set[str]
) -> list[tuple[str, ModuleResult, str]]:
    """Process the modules' interfaces in one SCC from source code."""
    # First verify if all transitive dependencies are loaded in the current process.
    t0 = time.time()
    maybe_load_deps(graph, ascc, manager)
    t1 = time.time()
    # Process the SCC in stable order.
    scc = order_ascc_ex(graph, ascc)

    t2 = time.time()
    stale = scc
    for id in stale:
        # Re-generate import errors in case this module was loaded from the cache.
        # Deserialized states all have meta=None, so the caller should specify
        # explicitly which of them are from cache.
        if id in from_cache:
            graph[id].verify_dependencies(suppressed_only=True)
    mypy.semanal_main.semantic_analysis_for_scc(graph, scc, manager.errors)

    t3 = time.time()
    # Track what modules aren't yet done, so we can finish them as soon
    # as possible, saving memory.
    unfinished_modules = set(stale)
    for id in stale:
        graph[id].type_check_first_pass(recurse_into_functions=False)
        if not graph[id].type_checker().deferred_nodes:
            unfinished_modules.discard(id)
    while unfinished_modules:
        for id in stale:
            if id not in unfinished_modules:
                continue
            if not graph[id].type_check_second_pass(recurse_into_functions=False):
                unfinished_modules.discard(id)

    t4 = time.time()
    scc_result = []
    meta_tuples = {}
    for id in stale:
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
        meta.dep_hashes = [
            graph[dep].interface_hash
            for dep in state.dependencies
            if state.priorities.get(dep) != PRI_INDIRECT
        ]
        write_cache_meta(meta, manager, meta_file)
        manager.commit_module(meta_file)
        scc_result.append((id, ModuleResult(graph[id].interface_hash.hex(), []), meta_file))
    manager.done_sccs.add(ascc.id)
    manager.add_stats(
        load_missing_time=t1 - t0,
        order_scc_time=t2 - t1,
        semanal_time=t3 - t2,
        type_check_time_interface=t4 - t3,
        flush_and_cache_time=time.time() - t4,
    )
    return scc_result

