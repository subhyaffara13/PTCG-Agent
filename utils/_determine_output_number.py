
def _determine_output_number(
    signature: ir.schemas.OpSignature, named_attrs: Mapping[str, ValidAttributeType]
) -> int:
    """Determine the number of outputs for the node with heuristics."""
    if signature.domain == "":
        if signature.name == "BatchNormalization":
            if not named_attrs.get("training_mode", 0):
                return 1
        if signature.name == "Split":
            num_outputs = named_attrs.get("num_outputs")
            if num_outputs is not None and isinstance(num_outputs, int):
                return num_outputs
            else:
                raise ValueError(
                    "Could not determine the number of outputs for Split. "
                    "num_outputs must be provided"
                )
    return len(signature.outputs)

