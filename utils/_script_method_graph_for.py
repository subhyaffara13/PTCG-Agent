
def _script_method_graph_for(self, parent, *args, **kwargs):
    try:
        dbs = parent.get_debug_state()
        eps = list(dbs.execution_plans.values())
        if len(eps) != 1:
            raise AssertionError(f"Expected exactly 1 execution plan, got {len(eps)}")
        graph = eps[0].graph.copy()

        # graph_executor_states for differentiable node
        fw_states = eps[0].code.differentiable_op_executor_states()
        diff_nodes: list[torch._C.Node] = []
        for n in graph.nodes():
            _get_differentiable_graph_node(n, diff_nodes)

        if len(fw_states) != len(diff_nodes):
            raise AssertionError(
                f"Expected fw_states ({len(fw_states)}) and diff_nodes "
                f"({len(diff_nodes)}) to have the same length"
            )
        # swap each differentiable graph with optimized graph in their execution plan
        for n, state in zip(diff_nodes, fw_states):
            fw_execution_plans = list(state.execution_plans.values())
            # we can only update the subgraph when there's a unique execution
            # plan. Avoid assert here so we would skip the ones that can't be
            # updated while try the best effort to update other nodes.
            if len(fw_execution_plans) == 1:
                n.g_("Subgraph", fw_execution_plans[0].graph)

        return graph
    except Exception:
        # fallback approach, we just ran the graph and return the recorded optimized
        # graph
        self(*args, **kwargs)
        return last_executed_optimized_graph()

