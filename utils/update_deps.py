
def update_deps(
    module_id: str,
    nodes: list[FineGrainedDeferredNode],
    graph: dict[str, State],
    deps: dict[str, set[str]],
    options: Options,
) -> None:
    for deferred in nodes:
        node = deferred.node
        type_map = graph[module_id].type_map()
        tree = graph[module_id].tree
        assert tree is not None, "Tree must be processed at this stage"
        new_deps = get_dependencies_of_target(
            module_id, tree, node, type_map, options.python_version
        )
        for trigger, targets in new_deps.items():
            deps.setdefault(trigger, set()).update(targets)
    # Merge also the newly added protocol deps (if any).
    type_state.update_protocol_deps(deps)

