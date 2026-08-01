
def _rewrite_dynamo_tensor_constants(
    orig_mod_buffers: set[torch.Tensor],
    traced_mod_buffers: dict[str, torch.Tensor],
    graph_signature: ExportGraphSignature,
    constants: dict[str, _ConstantAttributeType],
) -> None:
    """
    Dynamo erroneously marks tensor attributes on modules as buffers.
    Rewrite them to be tensor constants.
    """
    for spec in graph_signature.input_specs:
        if spec.kind == InputKind.BUFFER:
            if spec.target is None:
                raise AssertionError("spec.target must not be None for BUFFER kind")
            value = traced_mod_buffers[spec.target]
            if value not in orig_mod_buffers:
                # This was a tensor constant erroneously marked as a buffer.
                # Convert it into a constant in the graph signature, and add its
                # value to the constants table.
                spec.kind = InputKind.CONSTANT_TENSOR
                constants[spec.target] = value  # type: ignore[arg-type]

