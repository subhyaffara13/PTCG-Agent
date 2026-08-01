
def propagate_changes_using_dependencies(
    manager: BuildManager,
    graph: dict[str, State],
    deps: dict[str, set[str]],
    triggered: set[str],
    up_to_date_modules: set[str],
    targets_with_errors: set[str],
    processed_targets: list[str],
) -> list[tuple[str, str]]:
    """Transitively rechecks targets based on triggers and the dependency map.

    Returns a list (module id, path) tuples representing modules that contain
    a target that needs to be reprocessed but that has not been parsed yet.

    Processed targets should be appended to processed_targets (used in tests only,
    to test the order of processing targets).
    """

    num_iter = 0
    remaining_modules: list[tuple[str, str]] = []

    # Propagate changes until nothing visible has changed during the last
    # iteration.
    while triggered or targets_with_errors:
        num_iter += 1
        if num_iter > MAX_ITER:
            raise RuntimeError("Max number of iterations (%d) reached (endless loop?)" % MAX_ITER)

        todo, unloaded, stale_protos = find_targets_recursive(
            manager, graph, triggered, deps, up_to_date_modules
        )
        # TODO: we sort to make it deterministic, but this is *incredibly* ad hoc
        remaining_modules.extend((id, graph[id].xpath) for id in sorted(unloaded))
        # Also process targets that used to have errors, as otherwise some
        # errors might be lost.
        for target in targets_with_errors:
            id = module_prefix(graph, target)
            if id is not None and id not in up_to_date_modules:
                if id not in todo:
                    todo[id] = set()
                manager.log_fine_grained(f"process target with error: {target}")
                more_nodes, _ = lookup_target(manager, target, id)
                todo[id].update(more_nodes)
        triggered = set()
        # First invalidate subtype caches in all stale protocols.
        # We need to do this to avoid false negatives if the protocol itself is
        # unchanged, but was marked stale because its sub- (or super-) type changed.
        for info in stale_protos:
            type_state.reset_subtype_caches_for(info)
        # Then fully reprocess all targets.
        # TODO: Preserve order (set is not optimal)
        for id, nodes in sorted(todo.items(), key=lambda x: x[0]):
            assert id not in up_to_date_modules
            triggered |= reprocess_nodes(manager, graph, id, nodes, deps, processed_targets)
        # Changes elsewhere may require us to reprocess modules that were
        # previously considered up to date. For example, there may be a
        # dependency loop that loops back to an originally processed module.
        up_to_date_modules = set()
        targets_with_errors = set()
        if is_verbose(manager):
            manager.log_fine_grained(f"triggered: {list(triggered)!r}")

    return remaining_modules

