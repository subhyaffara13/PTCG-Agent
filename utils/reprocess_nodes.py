
def reprocess_nodes(
    manager: BuildManager,
    graph: dict[str, State],
    module_id: str,
    nodeset: set[FineGrainedDeferredNode],
    deps: dict[str, set[str]],
    processed_targets: list[str],
) -> set[str]:
    """Reprocess a set of nodes within a single module.

    Return fired triggers.
    """
    if module_id not in graph:
        manager.log_fine_grained("%s not in graph (blocking errors or deleted?)" % module_id)
        return set()

    file_node = manager.modules[module_id]
    old_symbols = find_symbol_tables_recursive(file_node.fullname, file_node.names)
    old_symbols = {name: names.copy() for name, names in old_symbols.items()}
    old_symbols_snapshot = snapshot_symbol_table(file_node.fullname, file_node.names)

    def key(node: FineGrainedDeferredNode) -> int:
        # Unlike modules which are sorted by name within SCC,
        # nodes within the same module are sorted by line number, because
        # this is how they are processed in normal mode.
        return node.node.line

    nodes = sorted(nodeset, key=key)

    state = graph[module_id]
    options = state.options
    manager.errors.set_file_ignored_lines(
        file_node.path, file_node.ignored_lines, options.ignore_errors or state.ignore_all
    )
    manager.errors.set_skipped_lines(file_node.path, file_node.skipped_lines)

    targets = set()
    for node in nodes:
        target = target_from_node(module_id, node.node)
        if target is not None:
            targets.add(target)
    manager.errors.clear_errors_in_targets(file_node.path, targets)

    # If one of the nodes is the module itself, emit any errors that
    # happened before semantic analysis.
    for target in targets:
        if target == module_id:
            for info in graph[module_id].early_errors:
                manager.errors.add_error_info(info, file=graph[module_id].xpath)

    # Strip semantic analysis information.
    for deferred in nodes:
        processed_targets.append(deferred.node.fullname)
        strip_target(deferred.node)
    semantic_analysis_for_targets(graph[module_id], nodes, graph)
    # Merge symbol tables to preserve identities of AST nodes. The file node will remain
    # the same, but other nodes may have been recreated with different identities, such as
    # NamedTuples defined using assignment statements.
    new_symbols = find_symbol_tables_recursive(file_node.fullname, file_node.names)
    for name in old_symbols:
        if name in new_symbols:
            merge_asts(file_node, old_symbols[name], file_node, new_symbols[name])

    # Type check.
    checker = graph[module_id].type_checker()
    checker.reset()
    # We seem to need additional passes in fine-grained incremental mode.
    checker.pass_num = 0
    checker.last_pass = 3
    # It is tricky to reliably invalidate constructor cache in fine-grained increments.
    # See PR 19514 description for details.
    more = checker.check_second_pass(nodes, allow_constructor_cache=False)
    while more:
        more = False
        if graph[module_id].type_checker().check_second_pass(allow_constructor_cache=False):
            more = True

    if manager.options.export_types:
        manager.all_types.update(graph[module_id].type_map())

    new_symbols_snapshot = snapshot_symbol_table(file_node.fullname, file_node.names)
    # Check if any attribute types were changed and need to be propagated further.
    changed = compare_symbol_table_snapshots(
        file_node.fullname, old_symbols_snapshot, new_symbols_snapshot
    )
    changed |= wildcard_triggers_for_changes(module_id, changed)
    new_triggered = {make_trigger(name) for name in changed}

    # Dependencies may have changed.
    update_deps(module_id, nodes, graph, deps, options)

    # Report missing imports.
    graph[module_id].verify_dependencies()

    graph[module_id].free_state()

    return new_triggered

