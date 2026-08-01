
def process_top_level_function(
    analyzer: SemanticAnalyzer,
    state: State,
    module: str,
    target: str,
    node: FuncDef | OverloadedFuncDef | Decorator,
    active_type: TypeInfo | None,
    patches: Patches,
) -> None:
    """Analyze single top-level function or method.

    Process the body of the function (including nested functions) again and again,
    until all names have been resolved (or iteration limit reached).
    """
    # We need one more iteration after incomplete is False (e.g. to report errors, if any).
    final_iteration = False
    incomplete = True
    # Start in the incomplete state (no missing names will be reported on first pass).
    # Note that we use module name, since functions don't create qualified names.
    deferred = [module]
    analyzer.deferral_debug_context.clear()
    analyzer.incomplete_namespaces.add(module)
    iteration = 0
    while deferred:
        iteration += 1
        if iteration == MAX_ITERATIONS:
            # Just pick some module inside the current SCC for error context.
            assert state.tree is not None
            with analyzer.file_context(state.tree, state.options):
                analyzer.report_hang()
            break
        if not (deferred or incomplete) or final_iteration:
            # OK, this is one last pass, now missing names will be reported.
            analyzer.incomplete_namespaces.discard(module)
        deferred, incomplete, progress = semantic_analyze_target(
            target, module, state, node, active_type, final_iteration, patches
        )
        if not incomplete:
            state.manager.incomplete_namespaces.discard(module)
        if final_iteration:
            assert not deferred, "Must not defer during final iteration"
        if not progress:
            final_iteration = True

    analyzer.incomplete_namespaces.discard(module)
    # After semantic analysis is done, discard local namespaces
    # to avoid memory hoarding.
    analyzer.saved_locals.clear()

