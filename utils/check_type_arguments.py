
def check_type_arguments(graph: Graph, scc: list[str], errors: Errors) -> None:
    for module in scc:
        state = graph[module]
        assert state.tree
        analyzer = TypeArgumentAnalyzer(
            errors,
            state.options,
            state.tree.is_typeshed_file(state.options),
            state.manager.semantic_analyzer.named_type,
        )
        with state.wrap_context():
            with mypy.state.state.strict_optional_set(state.options.strict_optional):
                state.tree.accept(analyzer)

