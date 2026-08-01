
def _override_graph_signature_for_temp_registered_constants(
    sig: "ExportGraphSignature", temp_registered_constants
):
    for spec in sig.input_specs:
        if spec.target in temp_registered_constants:
            spec.kind = InputKind.CONSTANT_TENSOR
            spec.persistent = None

    for spec in sig.output_specs:
        if (
            spec.kind == OutputKind.BUFFER_MUTATION
            and spec.target in temp_registered_constants
        ):
            raise RuntimeError(
                f"Constant {spec.target} is mutated in the forward method. Pls register it as buffer"
            )

    return sig

