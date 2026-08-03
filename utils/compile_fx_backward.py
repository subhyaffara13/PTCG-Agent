from typing import Callable

def compile_fx_backward(
    gm: GraphModule,
    example_inputs: Sequence[InputType],
    compiler_config_extra: CompilerConfigExtra,
    inner_compile: Callable[..., OutputCode] = compile_fx_inner,
) -> OutputCode:
    """
    Compile the backward graph of the given graph module.

    Args:
        gm: The graph module to compile.
        example_inputs: The example inputs to use for compilation.
        compiler_config_extra: Extra configuration for the compiler.
        inner_compile: The inner compile function to use.
    """
    from torch._dynamo.convert_frame import compile_lock

    with compile_lock:
        model_outputs_node = output_node(gm)
        if config.bw_outputs_user_visible:
            model_outputs = pytree.arg_tree_leaves(*model_outputs_node.args)
            model_outputs_node.meta["user_visible_output_idxs"] = [
                idx
                for idx, n in enumerate(model_outputs)
                if isinstance(n, torch.fx.Node)
            ]
        else:
            model_outputs_node.meta["user_visible_output_idxs"] = []

        fixed = count_tangents(gm)

        # Check if cudagraphs should be overridden for backward via annotation
        cudagraphs = compiler_config_extra.cudagraphs
        if compiler_config_extra.cudagraphs_bwd_override is not None:
            cudagraphs = BoxedBool(compiler_config_extra.cudagraphs_bwd_override)

        # When the forward was partitioned, saved activations from inline
        # code between partitions are NOT at fixed addresses. Only mark
        # primals (params/buffers) as static.
        if compiler_config_extra.forward_is_partitioned.value:
            static_input_idxs: Sequence[int] = get_static_bw_input_idxs(gm)
        else:
            static_input_idxs = list(range(fixed))
        with (
            (
                config.patch(get_cpp_wrapper_config())
                if config.cpp_wrapper
                else contextlib.nullcontext()
            ),
            cudagraph_annotation_context(cudagraphs),
        ):
            return inner_compile(
                gm,
                example_inputs,
                static_input_idxs=static_input_idxs,
                cudagraphs=cudagraphs,
                is_backward=True,
                graph_id=compiler_config_extra.graph_id,
                boxed_forward_device_index=compiler_config_extra.forward_device,
            )

