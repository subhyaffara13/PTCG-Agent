
def dump_inductor_provenance_info() -> dict[str, Any]:
    try:
        global _pre_grad_graph_id
        global _inductor_post_to_pre_grad_nodes
        global _inductor_triton_kernel_to_post_grad_node_info
        node_mapping: dict[str, Any] = {}
        if _pre_grad_graph_id:
            node_mapping_kernel = create_node_mapping_kernel_to_post_grad(
                _inductor_triton_kernel_to_post_grad_node_info
            )
            node_mapping = {
                **_inductor_post_to_pre_grad_nodes,
                **node_mapping_kernel,
            }
            if config.trace.enabled:
                with V.debug.fopen(
                    "inductor_provenance_tracking_node_mappings.json", "w"
                ) as fd:
                    json.dump(node_mapping, fd)
        # we need to update the node mapping version when node mapping format changes
        # so the tlparse tool knows which node mapping version it is looking at
        node_mapping["version"] = 2.0
        return node_mapping
    except Exception as e:
        # Since this is just debugging, it should never interfere with regular
        # program execution, so we use this try-except to guard against any error
        signpost_event(
            "inductor",
            "provenance_tracking_error",
            {
                "function": "dump_inductor_provenance_info",
                "error_msg": str(e),
                "stack_trace": traceback.format_exc(),
            },
        )
        return {}

