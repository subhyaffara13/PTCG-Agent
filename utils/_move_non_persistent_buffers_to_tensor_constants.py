
def _move_non_persistent_buffers_to_tensor_constants(
    orig_mod: torch.nn.Module,
    graph_signature: ExportGraphSignature,
    constants: dict[str, _ConstantAttributeType],
) -> None:
    """
    Moves non-persistent buffers to tensor constants.
    """
    for spec in graph_signature.input_specs:
        if spec.kind == InputKind.BUFFER and not spec.persistent:
            if spec.target is None:
                raise AssertionError(
                    "spec.target must not be None for non-persistent BUFFER kind"
                )
            if spec.target in constants:
                raise AssertionError(
                    f"spec.target {spec.target!r} should not already be in constants"
                )
            constants[spec.target] = orig_mod.get_buffer(spec.target)  # type: ignore[arg-type]

