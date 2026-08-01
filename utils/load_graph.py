
def load_graph(
    sources: list[BuildSource],
    manager: BuildManager,
    old_graph: Graph | None = None,
    new_modules: list[State] | None = None,
) -> Graph:
    """Given some source files, load the full dependency graph.

    If an old_graph is passed in, it is used as the starting point and
    modified during graph loading.

    If a new_modules is passed in, any modules that are loaded are
    added to the list. This is an argument and not a return value
    so that the caller can access it even if load_graph fails.

    As this may need to parse files, this can raise CompileError in case
    there are syntax errors.
    """

    graph: Graph = old_graph if old_graph is not None else {}

    # The deque is used to implement breadth-first traversal.
    # TODO: Consider whether to go depth-first instead.  This may
    # affect the order in which we process files within import cycles.
    new = new_modules if new_modules is not None else []
    entry_points: set[str] = set()
    # Seed the graph with the initial root sources.
    for bs in sources:
        try:
            st = State.new_state(
                id=bs.module,
                path=bs.path,
                source=bs.text,
                manager=manager,
                root_source=not bs.followed,
            )
        except ModuleNotFound:
            continue
        if st.id in graph:
            manager.errors.set_file(st.xpath, st.id, manager.options)
            manager.error(
                None,
                f'Duplicate module named "{st.id}" (also at "{graph[st.id].xpath}")',
                blocker=True,
            )
            resolution_note = f"""
            See {MODULE_RESOLUTION_URL} for more info
            Common resolutions include:
                a) using `--exclude` to avoid checking one of them,
                b) adding `__init__.py` somewhere,
                c) using `--explicit-package-bases` or adjusting `MYPYPATH`
            """
            manager.note_multiline(None, resolution_note)
            manager.errors.raise_error()
        graph[st.id] = st
        new.append(st)
        entry_points.add(bs.module)
    manager.parse_all([state for state in new if state.needs_parse])

    # Note: Running this each time could be slow in the daemon. If it's a problem, we
    # can do more work to maintain this incrementally.
    seen_files = {st.abspath: st for st in graph.values() if st.path}

    # Collect dependencies.  We go breadth-first.
    # More nodes might get added to new as we go, but that's fine.
    ready = set(new)
    # Use list to make syntax error order a bit more stable.
    not_ready: list[State] = []
    for st in new:
        if st not in ready:
            # We have run out of states, parse all we have.
            assert st in not_ready
            manager.parse_all(not_ready)
            ready.update(not_ready)
            not_ready.clear()
        assert st.ancestors is not None
        # Strip out indirect dependencies.  These will be dealt with
        # when they show up as direct dependencies, and there's a
        # scenario where they hurt:
        # - Suppose A imports B and B imports C.
        # - Suppose on the next round:
        #   - C is deleted;
        #   - B is updated to remove the dependency on C;
        #   - A is unchanged.
        # - In this case A's cached *direct* dependencies are still valid
        #   (since direct dependencies reflect the imports found in the source)
        #   but A's cached *indirect* dependency on C is wrong.
        dependencies = [dep for dep in st.dependencies if st.priorities.get(dep) != PRI_INDIRECT]
        if not manager.use_fine_grained_cache():
            added = [dep for dep in st.suppressed if find_module_simple(dep, manager)]
        else:
            # During initial loading we don't care about newly added modules,
            # they will be taken care of during fine-grained update. See also
            # comment about this in `State.new_state()`.
            added = []
        for dep in st.ancestors + dependencies + st.suppressed:
            ignored = dep in st.suppressed_set and dep not in entry_points
            if ignored and dep not in added:
                manager.missing_modules.setdefault(dep, SuppressionReason.NOT_FOUND)
                # TODO: for now we skip this in the daemon as a performance optimization.
                # This however creates a correctness issue, see #7777 and State.is_fresh().
                if not manager.use_fine_grained_cache() or manager.options.warn_unused_configs:
                    manager.import_options[dep] = manager.options.clone_for_module(
                        dep
                    ).dep_import_options()
            elif dep not in graph:
                try:
                    if dep in st.ancestors:
                        # TODO: Why not 'if dep not in st.dependencies' ?
                        # Ancestors don't have import context.
                        newst = State.new_state(
                            id=dep, path=None, source=None, manager=manager, ancestor_for=st
                        )
                    else:
                        newst = State.new_state(
                            id=dep,
                            path=None,
                            source=None,
                            manager=manager,
                            caller_state=st,
                            caller_line=st.dep_line_map.get(dep, 1),
                        )
                except ModuleNotFound:
                    if dep in st.dependencies_set:
                        st.suppress_dependency(dep)
                else:
                    if newst.path:
                        newst_path = newst.abspath

                        if newst_path in seen_files:
                            manager.errors.set_file(newst.xpath, newst.id, manager.options)
                            manager.error(
                                None,
                                "Source file found twice under different module names: "
                                f'"{seen_files[newst_path].id}" and "{newst.id}"',
                                blocker=True,
                            )
                            resolution_note = f"""
                            See {MODULE_RESOLUTION_URL} for more info
                            Common resolutions include:
                                a) adding `__init__.py` somewhere,
                                b) using `--explicit-package-bases` or adjusting `MYPYPATH`
                            """
                            manager.note_multiline(None, resolution_note)
                            manager.errors.raise_error()

                        seen_files[newst_path] = newst

                    assert newst.id not in graph, newst.id
                    graph[newst.id] = newst
                    new.append(newst)
                    if newst.needs_parse:
                        not_ready.append(newst)
                    else:
                        ready.add(newst)
    # There are two things we need to do after the initial load loop. One is up-suppress
    # modules that are back in graph. We need to do this after the loop to cover edge cases
    # like where a namespace package ancestor is shared by a typed and an untyped package.
    for st in graph.values():
        for dep in st.suppressed.copy():
            if dep in graph:
                st.add_dependency(dep)
                manager.missing_modules.pop(dep, None)
    # Second, in the initial loop we skip indirect dependencies, so to make indirect dependencies
    # behave more consistently with regular ones, we suppress them manually here (when needed).
    for st in graph.values():
        indirect = [dep for dep in st.dependencies if st.priorities.get(dep) == PRI_INDIRECT]
        for dep in indirect:
            if dep not in graph:
                st.suppress_dependency(dep)
    manager.plugin.set_modules(manager.modules)
    manager.errors.global_watcher = False
    return graph

