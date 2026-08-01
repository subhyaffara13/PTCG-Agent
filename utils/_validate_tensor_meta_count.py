
def _validate_tensor_meta_count(
    op_schema: OpSchema,
    tensor_meta: TensorMeta | Sequence[TensorMeta | None] | None,
) -> None:
    """
    Validate that the tensor_meta matches the expected number of outputs for the op.

    Raises AssertionError if the count doesn't match, providing a helpful error message.
    """
    expected_outputs = _get_expected_num_tensor_outputs(op_schema.op)

    # Compute actual count:
    # - None means 0 outputs
    # - TensorMeta (single instance) means 1 output
    # - Sequence of TensorMeta means len(sequence) outputs
    # Note: TensorMeta is a NamedTuple (subclass of tuple), so we must check for it first
    if tensor_meta is None:
        actual_outputs = 0
    elif isinstance(tensor_meta, TensorMeta):
        actual_outputs = 1
    else:
        actual_outputs = len(tensor_meta)

    if expected_outputs is None:
        # List[Tensor] return type: length unknown at schema time, but
        # tensor_meta must be a list of TensorMeta.
        if not isinstance(tensor_meta, list):
            raise AssertionError(
                f"Tensor meta for {op_schema.op} should be a list[TensorMeta] "
                f"(op returns List[Tensor]), but got {type(tensor_meta).__name__}"
            )
        return

    if actual_outputs != expected_outputs:
        raise AssertionError(
            f"Tensor meta count mismatch for {op_schema.op}: "
            f"expected {expected_outputs} tensor output(s) based on op schema, "
            f"but _propagate_tensor_meta returned {actual_outputs}. "
            f"This usually indicates a bug in fake tensor propagation for this op."
        )

