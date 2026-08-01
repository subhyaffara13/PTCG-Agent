
def _call_function_with_auto_output_flattening(
    tx: "InstructionTranslator",
    fn: Any,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    flat_example_value: Any,
    body_r: VariableTracker | None,
    graph_output_vts: VariableTracker | tuple[VariableTracker, ...],
    config: NestedCompileRegionOptions | None = None,
) -> VariableTracker | None:
    """
    Create HOP call node and reproxify output VTs for HOPs with auto output semantics.

    This function is used by HOPs with auto output semantics (see speculate_subgraph_with_auto_output_flattening)
    to create the actual HOP call in the FX graph and properly handle the output variable trackers.

    The key operation is "reproxifying" - updating the proxies of the original tensor VTs
    (from body_r) to point to the HOP call outputs, ensuring the outer graph correctly
    references the HOP outputs while allowing body_r to contain arbitrary Python objects.

    Args:
        tx: The instruction translator
        fn: The HOP function to call
        args: Arguments for the HOP call (typically includes the subgraph node)
        kwargs: Keyword arguments for the HOP call
        flat_example_value: Example value for the HOP output
        body_r: The output VT structure that Dynamo continues tracing with (may be None)
        graph_output_vts: Tensor/symint VTs that were actual graph outputs

    Returns:
        The body_r VT (unchanged), which Dynamo will continue tracing with
    """

    flat_variable = add_call_function(tx, fn, args, kwargs, flat_example_value, config)
    if body_r is not None:
        # pyrefly: ignore[bad-argument-type]
        overwrite_tensor_vt_proxy(graph_output_vts, flat_variable)
    return body_r

