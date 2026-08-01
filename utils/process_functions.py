
def process_functions(graph: Graph, scc: list[str], patches: Patches) -> None:
    # Process functions.
    all_targets = []
    for module in scc:
        tree = graph[module].tree
        assert tree is not None
        # In principle, functions can be processed in arbitrary order,
        # but _methods_ must be processed in the order they are defined,
        # because some features (most notably partial types) depend on
        # order of definitions on self.
        #
        # There can be multiple generated methods per line. Use target
        # name as the second sort key to get a repeatable sort order.
        targets = sorted(get_all_leaf_targets(tree), key=lambda x: (x[1].line, x[0]))
        all_targets.extend(
            [(module, target, node, active_type) for target, node, active_type in targets]
        )

    for module, target, node, active_type in order_by_subclassing(all_targets):
        analyzer = graph[module].manager.semantic_analyzer
        assert isinstance(node, (FuncDef, OverloadedFuncDef, Decorator)), node
        process_top_level_function(
            analyzer, graph[module], module, target, node, active_type, patches
        )

