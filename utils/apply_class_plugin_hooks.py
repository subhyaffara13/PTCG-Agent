
def apply_class_plugin_hooks(graph: Graph, scc: list[str], errors: Errors) -> None:
    """Apply class plugin hooks within a SCC.

    We run these after to the main semantic analysis so that the hooks
    don't need to deal with incomplete definitions such as placeholder
    types.

    Note that some hooks incorrectly run during the main semantic
    analysis pass, for historical reasons.
    """
    num_passes = 0
    incomplete = True
    # If we encounter a base class that has not been processed, we'll run another
    # pass. This should eventually reach a fixed point.
    while incomplete:
        assert num_passes < 10, "Internal error: too many class plugin hook passes"
        num_passes += 1
        incomplete = False
        for module in scc:
            state = graph[module]
            tree = state.tree
            assert tree
            with state.wrap_context():
                for _, node, _ in tree.local_definitions():
                    if isinstance(node.node, TypeInfo):
                        if not apply_hooks_to_class(
                            state.manager.semantic_analyzer,
                            module,
                            node.node,
                            state.options,
                            tree,
                            errors,
                        ):
                            incomplete = True

