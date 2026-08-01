
def load_states(
    mod_ids: list[str],
    graph: Graph,
    manager: BuildManager,
    import_errors: dict[str, list[ErrorInfo]],
    mod_data: dict[str, tuple[bytes, FileRawData | None]],
) -> None:
    """Re-create full state of an SCC as it would have been in coordinator."""
    if platform.python_implementation() == "CPython":
        # Run full collection after previous SCC batch, everything that survives
        # will be put into permanent generation below, since we don't free anything
        # after SCC processing is done.
        gc.collect()
        gc.disable()
    needs_parse = []
    for id in mod_ids:
        state = graph[id]
        # Re-clone options since we don't send them, it is usually faster than deserializing.
        state.options = state.options.clone_for_module(state.id)
        suppressed_deps_opts, raw_data = mod_data[id]
        if raw_data is not None:
            state.parse_file(raw_data=raw_data)
        else:
            needs_parse.append(state)
        # Set data that is needed to be written to cache meta.
        state.known_suppressed_deps_opts = suppressed_deps_opts
    # Perform actual parsing in parallel (but we don't need to compute dependencies).
    if needs_parse:
        manager.parse_all(needs_parse, post_parse=False)
    for id in mod_ids:
        state = graph[id]
        assert state.tree is not None
        import_lines = {imp.line for imp in state.tree.imports}
        state.imports_ignored = {
            line: codes for line, codes in state.tree.ignored_lines.items() if line in import_lines
        }
        # Replay original errors encountered during graph loading in coordinator.
        if id in import_errors:
            manager.errors.set_file(state.xpath, id, state.options)
            for err_info in import_errors[id]:
                manager.errors.add_error_info(err_info)
    if platform.python_implementation() == "CPython":
        gc.freeze()
        gc.enable()

