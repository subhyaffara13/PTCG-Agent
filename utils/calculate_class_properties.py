
def calculate_class_properties(graph: Graph, scc: list[str], errors: Errors) -> None:
    builtins = graph["builtins"].tree
    assert builtins
    for module in scc:
        state = graph[module]
        tree = state.tree
        assert tree
        for _, node, _ in tree.local_definitions():
            if isinstance(node.node, TypeInfo):
                with (
                    state.wrap_context(),
                    state.manager.semantic_analyzer.file_context(tree, state.options, node.node),
                ):
                    calculate_class_abstract_status(node.node, tree.is_stub, errors)
                    check_protocol_status(node.node, errors)
                    calculate_class_vars(node.node)
                    add_type_promotion(
                        node.node, tree.names, graph[module].options, builtins.names
                    )

