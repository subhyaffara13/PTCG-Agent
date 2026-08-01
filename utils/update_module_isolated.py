
def update_module_isolated(
    module: str,
    path: str,
    manager: BuildManager,
    previous_modules: dict[str, str],
    graph: Graph,
    force_removed: bool,
    followed: bool,
) -> UpdateResult:
    """Build a new version of one changed module only.

    Don't propagate changes to elsewhere in the program. Raise CompileError on
    encountering a blocking error.

    Args:
        module: Changed module (modified, created or deleted)
        path: Path of the changed module
        manager: Build manager
        graph: Build graph
        force_removed: If True, consider the module removed from the build even it the
            file exists

    Returns a named tuple describing the result (see above for details).
    """
    if module not in graph:
        manager.log_fine_grained(f"new module {module!r}")

    if not manager.fscache.isfile(path) or force_removed:
        delete_module(module, path, graph, manager)
        return NormalUpdate(module, path, [], None)

    sources = get_sources(manager.fscache, previous_modules, [(module, path)], followed)

    if module in manager.missing_modules:
        del manager.missing_modules[module]

    orig_module = module
    orig_state = graph.get(module)
    orig_tree = manager.modules.get(module)

    def restore(ids: list[str]) -> None:
        # For each of the modules in ids, restore that id's old
        # manager.modules and graphs entries. (Except for the original
        # module, this means deleting them.)
        for id in ids:
            if id == orig_module and orig_tree:
                manager.modules[id] = orig_tree
            elif id in manager.modules:
                del manager.modules[id]
            if id == orig_module and orig_state:
                graph[id] = orig_state
            elif id in graph:
                del graph[id]

    new_modules: list[State] = []
    try:
        if module in graph:
            del graph[module]
        load_graph(sources, manager, graph, new_modules)
    except CompileError as err:
        # Parse error somewhere in the program -- a blocker
        assert err.module_with_blocker
        restore([module] + [st.id for st in new_modules])
        return BlockedUpdate(err.module_with_blocker, path, [], err.messages)

    # Reparsing the file may have brought in dependencies that we
    # didn't have before. Make sure that they are loaded to restore
    # the invariant that a module having a loaded tree implies that
    # its dependencies do as well.
    ensure_trees_loaded(manager, graph, graph[module].dependencies)

    # Find any other modules brought in by imports.
    changed_modules = [(st.id, st.xpath) for st in new_modules]
    for m in new_modules:
        manager.import_map[m.id] = set(m.dependencies + m.suppressed)

    # If there are multiple modules to process, only process one of them and return
    # the remaining ones to the caller.
    if len(changed_modules) > 1:
        # As an optimization, look for a module that imports no other changed modules.
        module, path = find_relative_leaf_module(changed_modules, graph)
        changed_modules.remove((module, path))
        remaining_modules = changed_modules
        # The remaining modules haven't been processed yet so drop them.
        restore([id for id, _ in remaining_modules])
        manager.log_fine_grained(f"--> {module!r} (newly imported)")
    else:
        remaining_modules = []

    state = graph[module]

    # Process the changed file.
    state.parse_file()
    assert state.tree is not None, "file must be at least parsed"
    t0 = time.time()
    try:
        semantic_analysis_for_scc(graph, [state.id], manager.errors)
    except CompileError as err:
        # There was a blocking error, so module AST is incomplete. Restore old modules.
        restore([module])
        return BlockedUpdate(module, path, remaining_modules, err.messages)

    # Merge old and new ASTs.
    new_modules_dict: dict[str, MypyFile | None] = {module: state.tree}
    replace_modules_with_new_variants(manager, graph, {orig_module: orig_tree}, new_modules_dict)

    t1 = time.time()
    # Perform type checking.
    state.type_checker().reset()
    state.type_check_first_pass()
    state.type_check_second_pass()
    state.detect_possibly_undefined_vars()
    state.generate_unused_ignore_notes()
    state.generate_ignore_without_code_notes()
    t2 = time.time()
    state.finish_passes()
    t3 = time.time()
    manager.add_stats(semanal_time=t1 - t0, typecheck_time=t2 - t1, finish_passes_time=t3 - t2)

    graph[module] = state

    return NormalUpdate(module, path, remaining_modules, state.tree)

