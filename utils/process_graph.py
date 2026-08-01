
def process_graph(graph: Graph, manager: BuildManager) -> None:
    """Process everything in dependency order."""
    if manager.workers:
        # Commit any cache writes from graph loading before workers try to read them.
        manager.commit()

    # Broadcast graph to workers before computing SCCs to save a bit of time.
    # TODO: check if we can optimize by sending only part of the graph needed for given SCC.
    # For example only send modules in the SCC and their dependencies.
    graph_message = GraphMessage(graph=graph, missing_modules=manager.missing_modules)
    buf = WriteBuffer()
    graph_message.write(buf)
    graph_data = buf.getvalue()
    manager.wait_ack()
    manager.broadcast(graph_data)

    sccs = sorted_components(graph)
    manager.log(
        "Found %d SCCs; largest has %d nodes" % (len(sccs), max(len(scc.mod_ids) for scc in sccs))
    )
    scc_by_id = {scc.id: scc for scc in sccs}
    manager.scc_by_id = scc_by_id
    manager.top_order = [scc.id for scc in sccs]
    for scc in sccs:
        for mod_id in scc.mod_ids:
            manager.scc_by_mod_id[mod_id] = scc

    # Broadcast SCC structure to the parallel workers, since they don't compute it.
    sccs_message = SccsDataMessage(sccs=sccs)
    buf = WriteBuffer()
    sccs_message.write(buf)
    sccs_data = buf.getvalue()
    manager.wait_ack()
    manager.broadcast(sccs_data)
    manager.wait_ack()

    manager.free_workers = set(range(manager.options.num_workers))

    # Prime the ready list with leaf SCCs (that have no dependencies).
    ready = []
    not_ready = set()
    for scc in sccs:
        if not scc.deps:
            ready.append(scc)
        else:
            not_ready.add(scc)

    still_working = False
    while ready or not_ready or still_working:
        stale, fresh = find_stale_sccs(ready, graph, manager)
        if stale:
            for scc in stale:
                for id in scc.mod_ids:
                    graph[id].mark_as_rechecked()
            manager.submit(graph, stale)
            still_working = True
        # We eagerly walk over fresh SCCs to reach as many stale SCCs as soon
        # as possible. Only when there are no fresh SCCs, we wait on scheduled stale ones.
        # This strategy, similar to a naive strategy in minesweeper game, will allow us
        # to leverage parallelism as much as possible.
        if fresh:
            done = fresh
        else:
            done, still_working, results = manager.wait_for_done(graph)
            # Expose the results of type-checking by workers. For in-process
            # type-checking this is already done and results should be empty here.
            if not manager.workers:
                assert not results
            for id, result in results.items():
                # Interface and implementation results may be mixed in the same batch
                # from different workers, process each one accordingly.
                if result.interface_hash is not None:
                    new_hash = bytes.fromhex(result.interface_hash)
                    if new_hash != graph[id].interface_hash:
                        graph[id].mark_interface_stale()
                        graph[id].interface_hash = new_hash
                else:
                    manager.flush_errors(
                        manager.errors.simplify_path(graph[id].xpath), result.error_lines, False
                    )
        ready = []
        for done_scc in done:
            for dependent in done_scc.direct_dependents:
                dep_scc = scc_by_id[dependent]
                dep_scc.not_ready_count -= 1
                if not dep_scc.not_ready_count:
                    not_ready.remove(dep_scc)
                    ready.append(dep_scc)
    manager.trace(f"Transitive deps cache size: {sys.getsizeof(manager.transitive_deps_cache)}")

