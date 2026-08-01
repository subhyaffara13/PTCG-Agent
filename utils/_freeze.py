
def _freeze(
    dynamo_gm: torch.fx.GraphModule,
    aot_autograd_gm: torch.fx.GraphModule,
    example_inputs: list[torch._subclasses.FakeTensor],
) -> tuple[torch.fx.GraphModule, list[int]]:
    # We have convert conv's weight to channels last which may meet error for .view
    # when doing fake_tensor_prop. So we need to convert view to reshape first.
    # See the details in fx_codegen_and_compile of compile_fx.py.
    view_to_reshape(aot_autograd_gm)

    if tracing_context := torch._guards.TracingContext.try_get():
        fw_metadata = tracing_context.fw_metadata
        assert tracing_context.params_flat_unwrap_subclasses is not None
        params_flat = tracing_context.params_flat_unwrap_subclasses
        assert fw_metadata is not None and params_flat is not None

        preserved_arg_indices = replace_params_with_constants(
            aot_autograd_gm, params_flat, fw_metadata
        )
    else:
        inputs = aot_autograd_gm.graph.find_nodes(op="placeholder")
        preserved_arg_indices = list(range(len(inputs)))

    # TODO - further restrict cse ? right now needed to dedup aliasing ops
    cse_graph = fx_graph_cse(aot_autograd_gm.graph)
    aot_autograd_gm.graph = cse_graph
    aot_autograd_gm.recompile()

    aot_example_inputs = [example_inputs[ind] for ind in preserved_arg_indices]
    freezing_passes(aot_autograd_gm, aot_example_inputs)

    constant_fold(aot_autograd_gm)
    # invalidate nn Modules
    if config.freezing_discard_parameters:
        invalidate_eager_modules()
        discard_traced_gm_params(dynamo_gm)

    log.debug(
        "%s", lazy_format_graph_code("FROZEN GRAPH", aot_autograd_gm, colored=True)
    )

    record_has_frozen_params(aot_autograd_gm)
    return aot_autograd_gm, preserved_arg_indices

