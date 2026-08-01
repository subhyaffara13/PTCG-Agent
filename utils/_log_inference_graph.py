
def _log_inference_graph(
    fw_module: torch.fx.GraphModule,
    aot_config: AOTConfig,
) -> str | None:
    """
    Log the inference graph to the structured logger.
    Return a str representation of the graph.
    """
    if aot_config.enable_log:
        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "torch._functorch.config",
                "encoding": "string",
            },
            payload_fn=lambda: torch._functorch.config.get_serializable_config_copy(),
        )

    # Save the forward_graph_str right after aot_dispatch_base_graph,
    # to save in the cache
    aot_forward_graph_str = None
    if aot_config.cache_info is not None:
        aot_forward_graph_str = fw_module.print_readable(
            print_output=False,
            include_stride=True,
            include_device=True,
            fast_sympy_print=True,
            expanded_def=True,
        )

    return aot_forward_graph_str

