import time

def process_stale_scc_implementation(
    graph: Graph, stale: list[str], manager: BuildManager, meta_files: list[str]
) -> dict[str, ModuleResult]:
    """Process implementations (top-level function/method bodies) in an SCC."""
    t0 = time.time()
    unfinished_modules = set(stale)
    for id in stale:
        checker = graph[id].type_checker()
        # Optimization: if this is a 3rd party library, or we ignore errors
        # otherwise in this module, skip the implementations altogether.
        if checker.can_skip_diagnostics and not checker.options.preserve_asts:
            unfinished_modules.discard(id)
            graph[id].finish_passes()
            continue
        # We need to reset deferral count after possibly deferring any methods that
        # are considered part of the top-level (because they define/infer variables).
        checker.pass_num = 0
        checker.deferred_nodes.clear()
        tree = graph[id].tree
        assert tree is not None
        todo = []
        # Passing impl_only will select only "leaf" nodes (not the TypeInfos).
        for _, node, info in tree.local_definitions(impl_only=True):
            assert isinstance(node.node, (FuncDef, OverloadedFuncDef, Decorator))
            todo.append(DeferredNode(node.node, info))
        graph[id].type_check_second_pass(todo=todo, impl_only=True)
        if not checker.deferred_nodes:
            unfinished_modules.discard(id)
            graph[id].detect_possibly_undefined_vars()
            graph[id].finish_passes()
    while unfinished_modules:
        for id in stale:
            if id not in unfinished_modules:
                continue
            if not graph[id].type_check_second_pass(impl_only=True):
                unfinished_modules.discard(id)
                graph[id].detect_possibly_undefined_vars()
                graph[id].finish_passes()

    for id in stale:
        graph[id].generate_unused_ignore_notes()
        graph[id].generate_ignore_without_code_notes()

    scc_result = {}
    for id, meta_file in zip(stale, meta_files):
        state = graph[id]
        indirect = [dep for dep in state.dependencies if state.priorities.get(dep) == PRI_INDIRECT]
        meta_ex = CacheMetaEx(
            dependencies=indirect,
            suppressed=[
                dep for dep in state.suppressed if state.priorities.get(dep) == PRI_INDIRECT
            ],
            dep_hashes=[graph[dep].interface_hash for dep in indirect],
            error_lines=[],
        )
        if graph[id].xpath not in manager.errors.ignored_files:
            errors = manager.errors.file_messages(graph[id].xpath)
            formatted = manager.errors.format_messages(
                graph[id].xpath, errors, formatter=manager.error_formatter
            )
            meta_ex.error_lines = errors
            write_cache_meta_ex(meta_file, meta_ex, manager)
            scc_result[id] = ModuleResult(None, formatted)
        else:
            # If there are no errors, only write the cache, don't send anything back
            # to the caller (as a micro-optimization).
            write_cache_meta_ex(meta_file, meta_ex, manager)
        manager.commit_module(meta_file)

    manager.add_stats(type_check_time_implementation=time.time() - t0)
    return scc_result

