from typing import Any, Callable

def maybe_handle_backward_generation(
    compiled_graph: CompiledFxGraph,
    boxed_forward_device_index: BoxedDeviceIndex | None,
) -> None:
    assert compiled_graph.current_callable is not None
    is_backward = compiled_graph.fx_kwargs["is_backward"]

    # See [Backward Generation Handling]
    # if cudagraph'd the forward and set the device, we need to let the cudagraph manager
    # know we are we running the backward even if we will not run it in cudagraphs
    if is_backward and config.triton.cudagraph_trees:
        assert boxed_forward_device_index is not None
        assert boxed_forward_device_index.value is not None
        compiled_graph_callable = compiled_graph.current_callable

        manager = torch._inductor.cudagraph_trees.get_manager(
            boxed_forward_device_index.value, create_if_none_exists=False
        )
        # should already exist from forward
        assert manager is not None

        def compiled_artifact(new_inputs: list[Any]) -> Callable[..., Any]:
            manager.set_to_running_backward()  # type: ignore[union-attr]
            return compiled_graph_callable(new_inputs)

        compiled_graph.current_callable = compiled_artifact

