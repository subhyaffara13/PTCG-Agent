
def overwrite_tensor_vt_proxy(
    graph_output_vts: Iterable[VariableTracker], flat_variable: VariableTracker
) -> None:
    # wrap_fx_proxy creates fresh variable trackers. However, the main program
    # after the speculate subgraph can still use the original tensor vts that
    # are still pointing to the nodes present in the subgraph. So, we reproxify
    # the original tensor vts with the subgraph outputs. This way, whenever the
    # outer graph uses an original vt, it uses the subgraph output.
    #
    # This is critical for maintaining the separation between:
    # - `body_r`: The output VT structure that Dynamo continues tracing (may
    #   contain non-proxyable objects, nested structures, etc.)
    # - `graph_output_vts`: Only the tensor/symint VTs that were actual graph
    #   outputs from speculate_subgraph
    #
    # By overwriting the proxies of VTs in `body_r` with the proxies from the
    # HOP call, we ensure the outer graph correctly references the HOP outputs
    # while still allowing `body_r` to contain arbitrary Python objects.
    # pyrefly: ignore[missing-attribute]
    for orig_vt, subgraph_vt in zip(graph_output_vts, flat_variable.items):
        if isinstance(
            orig_vt,
            (
                variables.SymNodeVariable,
                variables.TensorVariable,
                TorchScriptObjectVariable,
            ),
        ):
            assert subgraph_vt.is_tensor() or isinstance(
                subgraph_vt, (SymNodeVariable, TorchScriptObjectVariable)
            )
            orig_vt.proxy = subgraph_vt.proxy

