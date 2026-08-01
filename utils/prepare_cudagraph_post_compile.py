
def prepare_cudagraph_post_compile(
    compiled_graph: CompiledFxGraph,
    example_inputs: Sequence[InputType],
    boxed_forward_device_index: BoxedDeviceIndex | None,
) -> None:
    if not config.triton.cudagraph_trees:
        # Force specialize all inputs so that CUDA graphs will work
        for t in example_inputs:
            if isinstance(t, torch.SymInt):
                int(t)  # guard

    is_inference = compiled_graph.fx_kwargs["is_inference"]
    is_backward = compiled_graph.fx_kwargs["is_backward"]
    if boxed_forward_device_index is not None and not is_inference and not is_backward:
        boxed_forward_device_index.set(next(iter(compiled_graph.device_idxs)))

