
def _recursive_pre_grad_passes(
    gm: GraphModule,
    example_inputs: Sequence[InputType],
) -> GraphModule:
    with dynamo_timed(
        "_recursive_pre_grad_passes",
        log_pt2_compile_event=True,
        dynamo_compile_column_us="pre_grad_pass_time_us",
    ):
        if not config.use_pre_grad_passes:
            return gm

        add_passes = config.add_pre_grad_passes
        remove_passes = config.remove_pre_grad_passes
        for subgraph_name in _get_subgraph_names(gm):
            subgraph = getattr(gm, subgraph_name)
            # as we don't have recursive example inputs, passing empty set here
            new_subgraph = _recursive_pre_grad_passes(subgraph, ())
            setattr(gm, subgraph_name, new_subgraph)
        return pre_grad_passes(gm, example_inputs, add_passes, remove_passes)

