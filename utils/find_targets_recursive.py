
def find_targets_recursive(
    manager: BuildManager,
    graph: Graph,
    triggers: set[str],
    deps: dict[str, set[str]],
    up_to_date_modules: set[str],
) -> tuple[dict[str, set[FineGrainedDeferredNode]], set[str], set[TypeInfo]]:
    """Find names of all targets that need to reprocessed, given some triggers.

    Returns: A tuple containing a:
     * Dictionary from module id to a set of stale targets.
     * A set of module ids for unparsed modules with stale targets.
    """
    result: dict[str, set[FineGrainedDeferredNode]] = {}
    worklist = triggers
    processed: set[str] = set()
    stale_protos: set[TypeInfo] = set()
    unloaded_files: set[str] = set()

    # Find AST nodes corresponding to each target.
    #
    # TODO: Don't rely on a set, since the items are in an unpredictable order.
    while worklist:
        processed |= worklist
        current = worklist
        worklist = set()
        for target in current:
            if target.startswith("<"):
                module_id = module_prefix(graph, trigger_to_target(target))
                if module_id:
                    ensure_deps_loaded(module_id, deps, graph)

                worklist |= deps.get(target, set()) - processed
            else:
                module_id = module_prefix(graph, target)
                if module_id is None:
                    # Deleted module.
                    continue
                if module_id in up_to_date_modules:
                    # Already processed.
                    continue
                if (
                    module_id not in manager.modules
                    or manager.modules[module_id].is_cache_skeleton
                ):
                    # We haven't actually parsed and checked the module, so we don't have
                    # access to the actual nodes.
                    # Add it to the queue of files that need to be processed fully.
                    unloaded_files.add(module_id)
                    continue

                if module_id not in result:
                    result[module_id] = set()
                manager.log_fine_grained(f"process: {target}")
                deferred, stale_proto = lookup_target(manager, target, module_id)
                if stale_proto:
                    stale_protos.add(stale_proto)
                result[module_id].update(deferred)

    return result, unloaded_files, stale_protos

