
def _recursive_post_grad_passes(gm: GraphModule, is_inference: bool = False) -> None:
    with dynamo_timed(
        "_recursive_post_grad_passes",
        log_pt2_compile_event=True,
        dynamo_compile_column_us="post_grad_pass_time_us",
    ):
        if not config.use_post_grad_passes:
            return

        for subgraph_name in _get_subgraph_names(gm):
            subgraph = getattr(gm, subgraph_name)
            _recursive_post_grad_passes(subgraph, is_inference)
        post_grad_passes(gm, is_inference)

