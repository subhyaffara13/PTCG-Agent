
def maybe_load_deps(graph: Graph, ascc: SCC, manager: BuildManager) -> None:
    """Load any missing fresh modules needed to process a stale SCC"""
    missing_sccs = set()
    sccs_to_find = ascc.deps.copy()
    while sccs_to_find:
        dep_scc = sccs_to_find.pop()
        if dep_scc in manager.done_sccs or dep_scc in missing_sccs:
            continue
        missing_sccs.add(dep_scc)
        sccs_to_find.update(manager.scc_by_id[dep_scc].deps)

    if missing_sccs:
        # Load missing SCCs from cache.
        # TODO: speed-up ordering if this causes problems for large builds.
        fresh_sccs_to_load = [
            manager.scc_by_id[sid] for sid in manager.top_order if sid in missing_sccs
        ]

        if manager.parallel_worker:
            # Update cache metas as well, cache data is loaded below
            # in process_fresh_modules().
            for prev_scc in fresh_sccs_to_load:
                for mod_id in prev_scc.mod_ids:
                    graph[mod_id].reload_meta()

        manager.log(f"Processing {len(fresh_sccs_to_load)} fresh SCCs")
        if (
            not manager.options.test_env
            and platform.python_implementation() == "CPython"
            and manager.gc_freeze_cycles < MAX_GC_FREEZE_CYCLES
        ):
            # When deserializing cache we create huge amount of new objects, so even
            # with our generous GC thresholds, GC is still doing a lot of pointless
            # work searching for garbage. So, we temporarily disable it when
            # processing fresh SCCs, and then move all the new objects to the oldest
            # generation with the freeze()/unfreeze() trick below. This is arguably
            # a hack, but it gives huge performance wins for large third-party
            # libraries, like torch.
            gc.disable()
        for prev_scc in fresh_sccs_to_load:
            manager.done_sccs.add(prev_scc.id)
            process_fresh_modules(graph, sorted(prev_scc.mod_ids), manager)
        if (
            not manager.options.test_env
            and platform.python_implementation() == "CPython"
            and manager.gc_freeze_cycles < MAX_GC_FREEZE_CYCLES
        ):
            manager.gc_freeze_cycles += 1
            gc.freeze()
            gc.unfreeze()
            gc.enable()

