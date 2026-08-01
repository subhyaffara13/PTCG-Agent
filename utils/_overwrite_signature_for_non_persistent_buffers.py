
def _overwrite_signature_for_non_persistent_buffers(
    old_sig: "ExportGraphSignature", new_sig: "ExportGraphSignature"
):
    # overwrite signature for non-persistent buffers
    non_persistent_buffers = {
        spec.target
        for spec in old_sig.input_specs
        if spec.kind == InputKind.BUFFER and not spec.persistent
    }

    for spec in new_sig.input_specs:
        if spec.kind == InputKind.BUFFER and spec.target in non_persistent_buffers:
            spec.persistent = False
    return new_sig

