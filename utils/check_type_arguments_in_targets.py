
def check_type_arguments_in_targets(
    targets: list[FineGrainedDeferredNode], state: State, errors: Errors
) -> None:
    """Check type arguments against type variable bounds and restrictions.

    This mirrors the logic in check_type_arguments() except that we process only
    some targets. This is used in fine grained incremental mode.
    """
    assert state.tree
    analyzer = TypeArgumentAnalyzer(
        errors,
        state.options,
        state.tree.is_typeshed_file(state.options),
        state.manager.semantic_analyzer.named_type,
    )
    with state.wrap_context():
        with mypy.state.state.strict_optional_set(state.options.strict_optional):
            for target in targets:
                func: FuncDef | OverloadedFuncDef | None = None
                if isinstance(target.node, (FuncDef, OverloadedFuncDef)):
                    func = target.node
                saved = (state.id, target.active_typeinfo, func)  # module, class, function
                with errors.scope.saved_scope(saved) if errors.scope else nullcontext():
                    analyzer.recurse_into_functions = func is not None
                    target.node.accept(analyzer)

