
def overwrite_tensor_vt_requires_grad(
    graph_output_vts: Iterable[VariableTracker], flat_variable: VariableTracker
) -> None:
    # All outputs of autograd.Function have requires_grad=True. We turn off
    # grad_mode in autograd.Function, so our outputs naively have
    # requires_grad=False. So we hackily force them back on here. A better
    # solution would be to write python code that Dynamo could trace but we
    # decided that it wasn't worth it.
    # pyrefly: ignore[missing-attribute]
    for orig_vt, subgraph_vt in zip(graph_output_vts, flat_variable.items):
        if isinstance(orig_vt, variables.TensorVariable):
            assert isinstance(subgraph_vt, variables.TensorVariable)
            orig_vt.requires_grad = subgraph_vt.requires_grad
            if orig_vt.requires_grad:
                orig_vt.has_grad_fn = True

