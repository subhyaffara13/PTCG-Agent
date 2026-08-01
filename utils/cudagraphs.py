
def cudagraphs(dynamo_model: torch.fx.GraphModule, dynamo_inputs: Sequence[Any]) -> Any:
    from torch._inductor.cudagraph_trees import cudagraphify_impl

    do_cudagraphs = BoxedBool(True)
    boxed_device_index = BoxedDeviceIndex(None)

    def forward_cudagraphs(
        aot_model: torch.fx.GraphModule,
        aot_inputs: list[Any],
        is_inference: bool = False,
    ) -> Any:
        interp = boxed_nop(aot_model, aot_inputs)
        fixed = num_fw_fixed_arguments(len(dynamo_inputs), len(aot_inputs))
        if skip_msg := check_for_skip(aot_model, fixed):
            BoxedBool.disable(do_cudagraphs)
            log_cudagraph_skip_and_bump_counter(
                f"skipping cudagraphs due to {skip_msg}"
            )
            return interp

        boxed_device_index.set(get_device_index(aot_model))
        out = cudagraphify_impl(
            interp,
            aot_inputs,
            range(fixed),
            device_index=boxed_device_index.value,
            is_backward=False,
            is_inference=is_inference,
            stack_traces=get_stack_traces(aot_model),
            placeholders=get_placeholder_info(aot_model.graph),
            mutated_input_idxs=find_input_mutations(aot_model.graph),
        )
        out._boxed_call = True  # type: ignore[attr-defined]
        return out

    def backward_cudagraphs(
        aot_model: torch.fx.GraphModule, aot_inputs: list[Any]
    ) -> Any:
        interp = boxed_nop(aot_model, aot_inputs)
        if not do_cudagraphs:
            return aot_model

        fixed = count_tangents(aot_model)
        if skip_msg := check_for_skip(aot_model, fixed):
            log_cudagraph_skip_and_bump_counter(
                f"skipping cudagraphs due to {skip_msg}"
            )

            # See [Backward Generation Handling]
            device_idx = boxed_device_index.value
            if device_idx is None:
                device_idx = 0  # Default to device 0 if not set
            manager = torch._inductor.cudagraph_trees.get_manager(
                device_idx, create_if_none_exists=False
            )
            assert manager is not None

            def fn(inputs: list[Any]) -> Any:
                # pyrefly: ignore [missing-attribute]
                manager.set_to_running_backward()
                return aot_model(inputs)

            fn._boxed_call = True  # type: ignore[attr-defined]
            return fn

        out = cudagraphify_impl(
            interp,
            aot_inputs,
            range(fixed),
            device_index=get_device_index(aot_model),
            is_backward=True,
            is_inference=False,
            stack_traces=get_stack_traces(aot_model),
            placeholders=get_placeholder_info(aot_model.graph),
            mutated_input_idxs=find_input_mutations(aot_model.graph),
        )
        out._boxed_call = True  # type: ignore[attr-defined]
        return out

    aot_cudagraphs = aot_autograd(
        fw_compiler=forward_cudagraphs,
        bw_compiler=backward_cudagraphs,
        inference_compiler=functools.partial(forward_cudagraphs, is_inference=True),
        keep_inference_input_mutations=torch._dynamo.config.cudagraph_backend_keep_input_mutation,
    )
    return aot_cudagraphs(dynamo_model, dynamo_inputs)

