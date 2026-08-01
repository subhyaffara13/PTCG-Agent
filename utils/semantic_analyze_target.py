
def semantic_analyze_target(
    target: str,
    module: str,
    state: State,
    node: MypyFile | FuncDef | OverloadedFuncDef | Decorator,
    active_type: TypeInfo | None,
    final_iteration: bool,
    patches: Patches,
) -> tuple[list[str], bool, bool]:
    """Semantically analyze a single target.

    Return tuple with these items:
    - list of deferred targets
    - was some definition incomplete (need to run another pass)
    - were any new names defined (or placeholders replaced)
    """
    state.manager.processed_targets.append((module, target))
    tree = state.tree
    assert tree is not None
    analyzer = state.manager.semantic_analyzer
    # TODO: Move initialization to somewhere else
    analyzer.global_decls = [set()]
    analyzer.nonlocal_decls = [set()]
    analyzer.globals = tree.names
    analyzer.imports = set()
    analyzer.progress = False
    with state.wrap_context(check_blockers=False):
        refresh_node = node
        if isinstance(refresh_node, Decorator):
            # Decorator expressions will be processed as part of the module top level.
            refresh_node = refresh_node.func
        analyzer.refresh_partial(
            refresh_node,
            patches,
            final_iteration,
            file_node=tree,
            options=state.options,
            active_type=active_type,
        )
        if isinstance(node, Decorator):
            infer_decorator_signature_if_simple(node, analyzer)

    # Clear out some stale data to avoid memory leaks and astmerge
    # validity check confusion
    analyzer.statement = None
    del analyzer.cur_mod_node

    if analyzer.deferred:
        return [target], analyzer.incomplete, analyzer.progress
    else:
        return [], analyzer.incomplete, analyzer.progress

