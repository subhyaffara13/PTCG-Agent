
def semantic_analysis_for_scc(graph: Graph, scc: list[str], errors: Errors) -> None:
    """Perform semantic analysis for all modules in a SCC (import cycle).

    Assume that reachability analysis has already been performed.

    The scc will be processed roughly in the order the modules are included
    in the list.
    """
    patches: Patches = []
    # Note that functions can't define new module-level attributes
    # using 'global x', since module top levels are fully processed
    # before functions. This limitation is unlikely to go away soon.
    process_top_levels(graph, scc, patches)
    process_functions(graph, scc, patches)
    # We use patch callbacks to fix up things when we expect relatively few
    # callbacks to be required.
    apply_semantic_analyzer_patches(patches)
    # Run class decorator hooks (they requite complete MROs and no placeholders).
    apply_class_plugin_hooks(graph, scc, errors)
    # This pass might need fallbacks calculated above and the results of hooks.
    check_type_arguments(graph, scc, errors)
    calculate_class_properties(graph, scc, errors)
    check_blockers(graph, scc)
    # Clean-up builtins, so that TypeVar etc. are not accessible without importing.
    if "builtins" in scc:
        cleanup_builtin_scc(graph["builtins"])

    # Report TypeForm profiling stats
    if len(scc) >= 1:
        # Get manager from any state in the SCC (they all share the same manager)
        manager = graph[scc[0]].manager
        analyzer = manager.semantic_analyzer
        manager.add_stats(
            type_expression_parse_count=analyzer.type_expression_parse_count,
            type_expression_full_parse_success_count=analyzer.type_expression_full_parse_success_count,
            type_expression_full_parse_failure_count=analyzer.type_expression_full_parse_failure_count,
        )

