import time

def serve(server: IPCServer, ctx: ServerContext) -> None:
    """Main server loop of the worker.

    Receive initial state from the coordinator, then process each
    SCC checking request and reply to client (coordinator). See module
    docstring for more details on the protocol.
    """
    buf = receive(server)
    if should_shutdown(buf, SOURCES_DATA_MESSAGE):
        return
    sources = SourcesDataMessage.read(buf).sources
    manager = setup_worker_manager(sources, ctx)
    if manager is None:
        return

    # Notify coordinator we are done with setup.
    send(server, AckMessage())
    buf = receive(server)
    if should_shutdown(buf, GRAPH_MESSAGE):
        return

    # Disable GC before loading graph and SCC structure, these create a bunch
    # of small objects that will stay around until the end of the build.
    if platform.python_implementation() == "CPython":
        gc.disable()

    graph_data = GraphMessage.read(buf, manager)
    # Update some manager data in-place as it has been passed to semantic analyzer.
    manager.missing_modules |= graph_data.missing_modules
    graph = graph_data.graph
    for id in graph:
        manager.import_map[id] = graph[id].dependencies_set
    # Link modules dicts, so that plugins will get access to ASTs as we parse them.
    manager.plugin.set_modules(manager.modules)

    # Notify coordinator we are ready to receive computed graph SCC structure.
    send(server, AckMessage())
    buf = receive(server)
    if should_shutdown(buf, SCCS_DATA_MESSAGE):
        return
    sccs = SccsDataMessage.read(buf).sccs
    manager.scc_by_id = {scc.id: scc for scc in sccs}
    manager.top_order = [scc.id for scc in sccs]

    if platform.python_implementation() == "CPython":
        gc.freeze()
        gc.enable()

    # Notify coordinator we are ready to start processing SCCs.
    send(server, AckMessage())
    while True:
        t0 = time.time()
        ready_to_read([server], WORKER_IDLE_TIMEOUT)
        t1 = time.time()
        buf = receive(server)
        assert read_tag(buf) == SCC_REQUEST_MESSAGE
        scc_message = SccRequestMessage.read(buf)
        manager.add_stats(scc_wait_time=t1 - t0, scc_receive_time=time.time() - t1)
        scc_ids = scc_message.scc_ids
        if not scc_ids:
            # This indicates a shutdown request. Add GC stats before exiting.
            gc_stats = gc.get_stats()
            manager.add_stats(
                gc_collections_gen0=gc_stats[0]["collections"],
                gc_collections_gen1=gc_stats[1]["collections"],
                gc_collections_gen2=gc_stats[2]["collections"],
            )
            manager.dump_stats()
            break
        sccs = [manager.scc_by_id[scc_id] for scc_id in scc_ids]
        mod_ids: list[str] = []
        for scc in sccs:
            mod_ids.extend(scc.mod_ids)
        t0 = time.time()
        try:
            load_states(mod_ids, graph, manager, scc_message.import_errors, scc_message.mod_data)
            results = []
            for scc in sccs:
                scc_result = process_stale_scc_interface(
                    graph, scc, manager, from_cache=graph_data.from_cache
                )
                results.extend(scc_result)
                # We must commit after each SCC, otherwise we break --sqlite-cache.
                manager.commit()
        except CompileError as blocker:
            message = SccResponseMessage(scc_ids=scc_ids, is_interface=True, blocker=blocker)
            timed_send(manager, server, message)
        else:
            mod_results = {}
            stale = []
            meta_files = []
            for id, mod_result, meta_file in results:
                stale.append(id)
                mod_results[id] = mod_result
                meta_files.append(meta_file)
            message = SccResponseMessage(scc_ids=scc_ids, is_interface=True, result=mod_results)
            timed_send(manager, server, message)
            try:
                # Process implementations one by one, so that we can free memory a bit earlier.
                result: dict[str, ModuleResult] = {}
                for id, meta_file in zip(stale, meta_files):
                    result |= process_stale_scc_implementation(graph, [id], manager, [meta_file])
                # Both phases write cache, so we should commit here as well.
                manager.commit()
            except CompileError as blocker:
                message = SccResponseMessage(scc_ids=scc_ids, is_interface=False, blocker=blocker)
            else:
                message = SccResponseMessage(scc_ids=scc_ids, is_interface=False, result=result)
            timed_send(manager, server, message)
        manager.add_stats(total_process_stale_time=time.time() - t0, stale_sccs_processed=1)

