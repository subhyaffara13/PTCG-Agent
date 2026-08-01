
def _recursive_joint_graph_passes(
    gm: GraphModule,
    skip_invoke_subgraph: bool = False,
    input_device: torch.device | None = None,
) -> GraphModule:
    def _run_on_sub_graph_module(subgraph_name: str) -> None:
        subgraph = getattr(gm, subgraph_name)
        new_subgraph = _recursive_joint_graph_passes(
            subgraph, skip_invoke_subgraph, input_device
        )
        setattr(gm, subgraph_name, new_subgraph)

    with dynamo_timed(
        "_recursive_joint_graph_passes",
        log_pt2_compile_event=True,
        dynamo_compile_column_us="joint_graph_pass_time_us",
    ):
        if not config.use_joint_graph_passes:
            return gm

        # invoke_subgraph already runs the _recursive_joint_graph_passes.  In
        # AOTAutograd, `run_joint_graph_passes_on_hops` partitions the
        # invoke_subgraph HOP before calling the partitioner on the outer graph.
        # AOTAutograd has access to partition_fn, which internally calls the
        # `_recursive_joint_graph_passes` for the subgraph. So, skip recursing
        # skip_invoke_subgraph.
        old_subgraph_names = OrderedSet(_get_subgraph_names(gm, skip_invoke_subgraph))
        for subgraph_name in old_subgraph_names:
            _run_on_sub_graph_module(subgraph_name)

        out_gm = joint_graph_passes(gm, input_device)

        # Some joint graph passes may create new sub graph module. Run one round
        # for the newly created graph modules.
        # We should not skip graphs for invoke_subgraph HOPs for newly
        # generated subgraphs.
        for subgraph_name in _get_subgraph_names(out_gm, skip_invoke_subgraph=False):
            if subgraph_name not in old_subgraph_names:
                _run_on_sub_graph_module(subgraph_name)
        return out_gm

