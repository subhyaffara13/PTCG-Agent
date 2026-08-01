
def semantic_analysis_for_targets(
    state: State, nodes: list[FineGrainedDeferredNode], graph: Graph
) -> None:
    """Semantically analyze only selected nodes in a given module.

    This essentially mirrors the logic of semantic_analysis_for_scc()
    except that we process only some targets. This is used in fine-grained
    incremental mode, when propagating an update.
    """
    patches: Patches = []
    if any(isinstance(n.node, MypyFile) for n in nodes):
        # Process module top level first (if needed).
        process_top_levels(graph, [state.id], patches)
    analyzer = state.manager.semantic_analyzer
    for n in nodes:
        if isinstance(n.node, MypyFile):
            # Already done above.
            continue
        process_top_level_function(
            analyzer, state, state.id, n.node.fullname, n.node, n.active_typeinfo, patches
        )
    apply_semantic_analyzer_patches(patches)
    apply_class_plugin_hooks(graph, [state.id], state.manager.errors)
    check_type_arguments_in_targets(nodes, state, state.manager.errors)
    calculate_class_properties(graph, [state.id], state.manager.errors)

