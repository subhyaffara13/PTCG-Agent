
def _call_symbolic_op(
    op_type: str,
    domain: str,
    args: Sequence[ir.Value | None],
    kwargs: dict[str, int | float | str | bool | list[int] | list[float] | list[str]],
    dtypes: Sequence[int],
    version: int | None,
    metadata_props: dict[str, str] | None,
) -> Sequence[ir.Value]:
    """Call an operator with the given arguments and keyword arguments.

    Arguments are always inputs, while keyword arguments are attributes.
    """
    # This is a wrapper around the IR node creation that hooks into the _builder.OpRecorder
    # tracer so that all nodes created are recorded the same way as if we were to use
    # onnxscript ops directly.

    if _core.current_tracer is None:
        raise AssertionError("current_tracer must be non-None")
    tracer = _core.current_tracer

    inputs = list(args)

    # If final inputs are None, strip them from the node inputs
    for input in reversed(inputs):
        if input is not None:
            break
        inputs.pop()

    # Construct and filter out None attributes
    attributes = [
        attr
        for attr in ir_convenience.convert_attributes(kwargs)  # type: ignore[arg-type]
        if attr.value is not None  # type: ignore[union-attr]
    ]
    tracer.nodes.append(
        node := ir.Node(
            domain,
            op_type,
            inputs=inputs,
            attributes=attributes,
            num_outputs=len(dtypes),
            version=version,
            metadata_props=metadata_props,
        )
    )
    # Set the dtypes for the outputs. We set them here because the graph builder
    # Uses PyTorch types which are sometimes inaccurate when they are ONNX only
    # types like float4e2m1.
    for value, dtype in zip(node.outputs, dtypes):
        value.dtype = ir.DataType(dtype)
        # The shape is set by the graph builder. We don't need to set it here.
    return node.outputs

