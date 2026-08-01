
def _optimize_runtime_with_given_memory(
    joint_graph: fx.Graph,
    memory: list[float],
    runtimes: list[float],
    max_memory: float,
    node_info: NodeInfo,
    all_recomputable_banned_nodes: list[fx.Node],
) -> tuple[float, list[int], list[int]]:
    SOLVER = config.activation_memory_budget_solver
    if SOLVER == "greedy":
        return greedy_knapsack(memory, runtimes, max_memory)
    elif SOLVER == "ilp":
        return ilp_knapsack(memory, runtimes, max_memory)
    elif SOLVER == "dp":
        return dp_knapsack(memory, runtimes, max_memory)
    elif SOLVER == "dp_knapsack_sliding_hirschberg":
        return dp_knapsack_sliding_hirschberg(memory, runtimes, max_memory)
    elif SOLVER == "dynamic_memory_budget_dp":
        log.warning(
            "dynamic_memory_budget_dp is an experimental solver. "
            "It does not guarantee performance improvements. "
            "Additionally, it is not guaranteed to be stable."
        )
        graph_info_provider = GraphInfoProvider.inialize_from_graph(
            joint_graph=joint_graph,
            all_recomputable_banned_nodes=all_recomputable_banned_nodes,
            recorded_knapsack_input_memories=memory,
            recorded_knapsack_input_runtimes=runtimes,
        )
        return dp_knapsack(
            memory,
            runtimes,
            KnapsackEvaluator(
                graph_info_provider=graph_info_provider,
            ).get_knee_point_memory_budget(
                knapsack_algo=dp_knapsack,
                max_mem_budget=max_memory,
            ),
        )
    elif isinstance(SOLVER, CustomKnapsackSolver):
        saved_node_idx, recomp_node_idx = SOLVER(
            memory, joint_graph, max_memory, node_info, all_recomputable_banned_nodes
        )
        return (0.0, saved_node_idx, recomp_node_idx)
    else:
        raise RuntimeError(f"Not aware of memory budget knapsack solver: {SOLVER}")

