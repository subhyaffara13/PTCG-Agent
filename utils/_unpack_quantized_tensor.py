
def _unpack_quantized_tensor(tuple_value: _C.Value) -> tuple[_C.Value, ...]:
    """Unpacks a quantized tensor into a tuple of tensor and scale/zero_point.
    Args:
        tuple_value: A tuple of tensor, scale, zero_point, and optionally axis.
    Returns:
        A tuple of tensor, scale, zero_point, and optionally axis.
    """
    tuple_node = tuple_value.node()
    # A quantized tensor is represented as tuple of the form (tensor, scale, zero_point, <axis>)
    if not _is_tuple_construct(tuple_value):
        raise errors.SymbolicValueError(
            f"ONNX symbolic expected the output of `{tuple_node}` to be a quantized "
            f"tensor. Is this likely due to missing support for quantized "
            f"`{tuple_node.kind()}`. Please create an issue on {_constants.PYTORCH_GITHUB_ISSUES_URL}",
            tuple_value,
        )
    unpacked = tuple(tuple_node.inputs())
    if not (len(unpacked) == 3 or len(unpacked) == 4):
        raise AssertionError(f"Expected 3 or 4 elements, got {len(unpacked)}")
    return unpacked

