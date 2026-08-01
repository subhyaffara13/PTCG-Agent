
def compile_fx_inner(
    gm: GraphModule,
    example_inputs: Sequence[InputType],
    compile_region_name: str | None = None,
    **kwargs: Unpack[_CompileFxKwargs],
) -> OutputCode:
    kwargs.setdefault("cudagraphs", None)
    kwargs.setdefault("static_input_idxs", ())
    kwargs.setdefault("is_backward", False)
    kwargs.setdefault("graph_id", None)
    kwargs.setdefault("cpp_wrapper", False)
    kwargs.setdefault("fx_wrapper", False)
    kwargs.setdefault("is_inference", False)
    kwargs.setdefault("boxed_forward_device_index", None)
    kwargs.setdefault("layout_opt", None)
    kwargs.setdefault("extern_node_serializer", None)

    # Need with_fresh_cache_if_config for compile_fx_inner even if we already have one for
    # compile_fx. The reason is the compilation for backward graph may happen after
    # compile_fx return and we may want to use the _LazyGraphModule for compiling
    # the backward graph as well.
    with contextlib.ExitStack() as stack:
        stack.enter_context(torch.utils._python_dispatch._disable_current_modes())
        stack.enter_context(_use_lazy_graph_module(dynamo_config.use_lazy_graph_module))
        stack.enter_context(
            dynamo_utils.dynamo_timed(
                "compile_fx_inner",
                phase_name="inductor_compile",
                log_pt2_compile_event=True,
                log_waitcounter=True,
                waitcounter_name_override="compile_inductor",
                dynamo_compile_column_us="inductor_cumulative_compile_time_us",
            )
        )
        stack.enter_context(with_fresh_cache_if_config())
        stack.enter_context(DebugContext())
        CompileEventLogger.pt2_compile(
            "inductor_compile",
            is_backward=kwargs["is_backward"],
        )
        return wrap_compiler_debug(_compile_fx_inner, compiler_name="inductor")(
            gm,
            example_inputs,
            compile_region_name=compile_region_name,
            **kwargs,
        )

