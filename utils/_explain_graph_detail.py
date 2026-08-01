
def _explain_graph_detail(
    gm: torch.fx.GraphModule,
    graphs: list[torch.fx.GraphModule],
    op_count: int,
    ops_per_graph: list[list["Target"]],
    break_reasons: list[GraphCompileReason],
) -> tuple[
    torch.fx.GraphModule,
    list[torch.fx.GraphModule],
    int,
    list[list["Target"]],
    list[GraphCompileReason],
]:
    """
    This function is a utility which processes a torch.fx.GraphModule and
    accumulates information about its ops, graph breaks, and other details. It
    is intended to be used by the ExplainWithBackend class and
    `torch._dynamo.explain()` to provide details from Dynamo's graph capture.

    Parameters:
        gm (torch.fx.GraphModule): The GraphModule to be processed.
        graphs (list): A list that accumulates all the GraphModules processed.
        op_count (int): The total count of operations in all GraphModules processed so far.
        ops_per_graph (list): A list that accumulates the operations of each GraphModule.
        break_reasons (list): A list that accumulates the reasons for breaks in each GraphModule.

    Returns:
        tuple: A tuple containing the processed GraphModule, the updated lists of graphs,
               operations per graph, and break reasons, and the updated operation count.
    """
    graphs.append(gm)
    ops = [node.target for node in gm.graph.nodes if node.op == "call_function"]
    op_count += len(ops)
    ops_per_graph.append(ops)
    if gm.compile_subgraph_reason.graph_break:  # type: ignore[union-attr]
        break_reasons.append(gm.compile_subgraph_reason)  # type: ignore[arg-type]

    return gm, graphs, op_count, ops_per_graph, break_reasons

