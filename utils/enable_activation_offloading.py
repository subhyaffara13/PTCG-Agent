
def enable_activation_offloading(
    fwd_module: fx.GraphModule,
    bwd_module: fx.GraphModule,
    num_fwd_outputs: int,
    static_lifetime_input_nodes: OrderedSet[fx.Node],
) -> None:
    """
    Main entry point for activation offloading.

    Args:
        fwd_module: Forward module graph
        bwd_module: Backward module graph
        num_fwd_outputs: Number of forward outputs
    """

    # Step 1: Decide which nodes to offload and mark them
    should_perform_offloading: bool = choose_offload_sets(
        fwd_module,
        num_fwd_outputs,
        static_lifetime_input_nodes,
    )
    if not should_perform_offloading:
        return

    # Step 2: Add offload and reload nodes to the graphs
    if config.activation_offload_separate_stream:
        # Use async ao ops (2 nodes each: offload/reload + wait_tensor)
        offload_chosen_sets_async(fwd_module, bwd_module)
        if config.activation_offload_sink_wait:
            activation_offload_sink_wait_async(fwd_module)
        if config.activation_reload_prefetch:
            activation_reload_prefetch_async(bwd_module)
    else:
        # Use synchronous device_put (1 node each)
        offload_chosen_sets(fwd_module, bwd_module)

    fwd_module.graph.lint()
    bwd_module.graph.lint()

