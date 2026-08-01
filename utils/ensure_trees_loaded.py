
def ensure_trees_loaded(
    manager: BuildManager, graph: dict[str, State], initial: Sequence[str]
) -> None:
    """Ensure that the modules in initial and their deps have loaded trees."""
    to_process = find_unloaded_deps(manager, graph, initial)
    if to_process:
        if is_verbose(manager):
            manager.log_fine_grained(
                "Calling process_fresh_modules on set of size {} ({})".format(
                    len(to_process), sorted(to_process)
                )
            )
        process_fresh_modules(graph, to_process, manager)

