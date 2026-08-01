
def _log_fw_bw_graphs(
    fw_module: torch.fx.GraphModule,
    bw_module: torch.fx.GraphModule,
    maybe_subclass_meta: SubclassMeta | None,
    fw_metadata: ViewAndMutationMeta,
    aot_config: AOTConfig,
) -> tuple[str | None, str | None]:
    """
    Log the fw and bw graphs to the structured logger.
    Return str representations of the graphs.
    """
    fw_module_str = None
    bw_module_str = None
    if aot_config.enable_log:
        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "torch._functorch.config",
                "encoding": "string",
            },
            payload_fn=lambda: torch._functorch.config.get_serializable_config_copy(),
        )
        aot_graphs_log.info(
            "aot_config id: %s, fw_metadata=%s, inner_meta=%s",
            aot_config.aot_id,
            fw_metadata,
            _get_inner_meta(maybe_subclass_meta, fw_metadata),
        )

        aot_graphs_log.info(
            "%s",
            lazy_format_graph_code(
                "Forward graph",
                fw_module,
                aot_config.aot_id,
                include_stride=True,
                include_device=True,
                colored=True,
            ),
        )
        aot_graphs_log.info(
            "%s",
            lazy_format_graph_code(
                "Backward graph",
                bw_module,
                aot_config.aot_id,
                include_stride=True,
                include_device=True,
                colored=True,
            ),
        )
        fw_module_str = fw_module.print_readable(
            print_output=False,
            include_stride=True,
            include_device=True,
            expanded_def=True,
        )
        bw_module_str = bw_module.print_readable(
            print_output=False,
            include_stride=True,
            include_device=True,
            expanded_def=True,
        )

        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "aot_forward_graph_fw_metadata",
                "encoding": "string",
            },
            payload_fn=lambda: dataclass_repr(fw_metadata),
        )
        if maybe_subclass_meta is not None:
            trace_structured(
                "artifact",
                metadata_fn=lambda: {
                    "name": "aot_forward_graph_fw_subclass_metadata",
                    "encoding": "string",
                },
                payload_fn=lambda: dataclass_repr(maybe_subclass_meta),
            )

        trace_structured(
            "aot_forward_graph",
            payload_fn=lambda: fw_module_str,
        )
        trace_structured(
            "aot_backward_graph",
            payload_fn=lambda: bw_module_str,
        )
    return fw_module_str, bw_module_str

