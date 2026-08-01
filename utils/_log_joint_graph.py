
def _log_joint_graph(
    fx_g: torch.fx.GraphModule,
    aot_config: AOTConfig,
) -> str | None:
    """
    Log the joint graph to the structured logger.
    Return a str representation of the graph.
    """
    joint_graph_str = None
    if aot_config.enable_log:
        aot_joint_log.info(
            "%s",
            lazy_format_graph_code(
                "Joint graph",
                fx_g,
                aot_config.aot_id,
                include_stride=True,
                include_device=True,
                colored=True,
            ),
        )
        joint_graph_str = fx_g.print_readable(
            print_output=False,
            include_stride=True,
            include_device=True,
            expanded_def=True,
        )
        trace_structured(
            "aot_joint_graph",
            payload_fn=lambda: joint_graph_str,
        )
    return joint_graph_str

