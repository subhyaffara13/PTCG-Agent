
def higher_order_invoke_subgraph(
    subgraph: ir.Function,
    identifier: str | None,
    *operands: ir.Value,
) -> Sequence[ir.Value]:
    """Export invoke_subgraph HOP by creating a direct function call.

    This preserves the function as a separate entity in the ONNX graph
    instead of inlining it, which is the purpose of invoke_subgraph.

    Note: The onnxscript optimizer should be configured to not inline functions
    created by invoke_subgraph to preserve the intended structure.

    Args:
        subgraph: The function to invoke
        identifier: Optional identifier for the subgraph (used for caching in PyTorch,
            not needed for ONNX export as the function reference provides all necessary information)
        *operands: Input values to pass to the function

    Returns:
        Sequence of output values from the function call
    """
    # This key can be used by downstream to avoid inlining
    subgraph.metadata_props["pkg.torch.ops.higher_order.invoke_subgraph.identifier"] = (
        str(identifier)
    )

    # Create the function call node
    return call_op(
        subgraph.name,
        *operands,
        _num_outputs=len(subgraph.outputs),
        _domain=subgraph.domain,
    )

