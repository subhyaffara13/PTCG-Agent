
def find_stale_sccs(
    sccs: list[SCC], graph: Graph, manager: BuildManager
) -> tuple[list[SCC], list[SCC]]:
    """Split a list of ready SCCs into stale and fresh.

    Fresh SCCs are those where:
    * We have valid cache files for all modules in the SCC.
    * There are no changes in dependencies (files removed from/added to the build).
    * The interface hashes of dependencies matches those recorded in the cache.
    * All indirect dependencies are still reachable via direct ones.
    The first and second conditions are verified by is_fresh().
    """
    stale_sccs = []
    fresh_sccs = []
    for ascc in sccs:
        stale_scc = {id for id in ascc.mod_ids if not graph[id].is_fresh()}
        fresh = not stale_scc

        # Verify that interfaces of dependencies still present in graph are up-to-date (fresh).
        stale_deps = set()
        for id in ascc.mod_ids:
            for dep in graph[id].dep_hashes:
                if dep in graph and graph[dep].interface_hash != graph[id].dep_hashes[dep]:
                    stale_deps.add(dep)
        fresh = fresh and not stale_deps

        # Verify the invariant that indirect dependencies are a subset of transitive direct
        # dependencies. Note: the case where indirect dependency is removed from the graph
        # completely is already handled above.
        stale_indirect = None
        if fresh:
            stale_indirect = verify_transitive_deps(ascc, graph, manager)
            if stale_indirect is not None:
                fresh = False

        if manager.logging_enabled:
            if fresh:
                fresh_msg = "fresh"
            elif stale_scc:
                fresh_msg = "inherently stale"
                if stale_scc != ascc.mod_ids:
                    fresh_msg += f" ({' '.join(sorted(stale_scc))})"
                if stale_deps:
                    fresh_msg += f" with stale deps ({' '.join(sorted(stale_deps))})"
            elif stale_deps:
                fresh_msg = f"stale due to deps ({' '.join(sorted(stale_deps))})"
            else:
                assert stale_indirect is not None
                fresh_msg = f"stale due to stale indirect dep(s): first {stale_indirect}"
            scc_str = " ".join(ascc.mod_ids)

        if fresh:
            if manager.tracing_enabled:
                manager.trace(f"Found {fresh_msg} SCC ({scc_str})")
            # If there is at most one file with errors we can skip the ordering to save time.
            mods_with_errors = [id for id in ascc.mod_ids if graph[id].error_lines]
            if len(mods_with_errors) <= 1:
                scc = mods_with_errors
            else:
                # Use exactly the same order as for stale SCCs for stability.
                scc = order_ascc_ex(graph, ascc)
            for id in scc:
                if graph[id].error_lines:
                    path = manager.errors.simplify_path(graph[id].xpath)
                    formatted = manager.errors.format_messages(
                        path, graph[id].error_lines, formatter=manager.error_formatter
                    )
                    manager.flush_errors(path, formatted, False)
            fresh_sccs.append(ascc)
        else:
            if manager.logging_enabled:
                size = len(ascc.mod_ids)
                if size == 1:
                    manager.log(f"Scheduling SCC singleton ({scc_str}) as {fresh_msg}")
                else:
                    manager.log(
                        "Scheduling SCC of size %d (%s) as %s" % (size, scc_str, fresh_msg)
                    )
            stale_sccs.append(ascc)
    return stale_sccs, fresh_sccs

