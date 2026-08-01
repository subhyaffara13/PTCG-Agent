
def process_top_levels(graph: Graph, scc: list[str], patches: Patches) -> None:
    # Process top levels until everything has been bound.

    # Reverse order of the scc so the first modules in the original list will be
    # be processed first. This helps with performance.
    scc = list(reversed(scc))  # noqa: FURB187 intentional copy

    # Initialize ASTs and symbol tables.
    for id in scc:
        state = graph[id]
        assert state.tree is not None
        state.manager.semantic_analyzer.prepare_file(state.tree)

    # Initially all namespaces in the SCC are incomplete (well they are empty).
    state.manager.incomplete_namespaces.update(scc)

    worklist = scc.copy()
    # HACK: process core stuff first. This is mostly needed to support defining
    # named tuples in builtin SCC.
    if all(m in worklist for m in core_modules):
        worklist += list(reversed(core_modules)) * CORE_WARMUP
    final_iteration = False
    iteration = 0
    analyzer = state.manager.semantic_analyzer
    analyzer.deferral_debug_context.clear()

    while worklist:
        iteration += 1
        if iteration > MAX_ITERATIONS:
            # Just pick some module inside the current SCC for error context.
            assert state.tree is not None
            with analyzer.file_context(state.tree, state.options):
                analyzer.report_hang()
            break
        if final_iteration:
            # Give up. It's impossible to bind all names.
            state.manager.incomplete_namespaces.clear()
        all_deferred: list[str] = []
        any_progress = False
        while worklist:
            next_id = worklist.pop()
            state = graph[next_id]
            assert state.tree is not None
            deferred, incomplete, progress = semantic_analyze_target(
                next_id, next_id, state, state.tree, None, final_iteration, patches
            )
            all_deferred += deferred
            any_progress = any_progress or progress
            if not incomplete:
                state.manager.incomplete_namespaces.discard(next_id)
        if final_iteration:
            assert not all_deferred, "Must not defer during final iteration"
        # Reverse to process the targets in the same order on every iteration. This avoids
        # processing the same target twice in a row, which is inefficient.
        worklist = list(reversed(all_deferred))
        final_iteration = not any_progress
    # Functions/methods that define/infer attributes are processed as part of top-levels.
    # We need to clear the locals for those between fine-grained iterations.
    analyzer.saved_locals.clear()

