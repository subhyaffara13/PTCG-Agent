
def _create_graph_and_save_traced_inputs(
    fn_to_trace: Callable[..., Any],
    flat_args: Any,
    flat_args_descs: Any,
    *,
    aot_config: AOTConfig,
) -> tuple[torch.fx.GraphModule, Any]:
    saved_flat_args = _detach_traced_inputs(flat_args)
    return (
        _create_graph(fn_to_trace, flat_args, flat_args_descs, aot_config=aot_config),
        saved_flat_args,
    )

