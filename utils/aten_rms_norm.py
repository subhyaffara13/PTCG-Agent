
def aten_rms_norm(
    input: TFloat,
    normalized_shape: Sequence[int],
    weight: TFloat | None = None,
    eps: float | None = None,
) -> TFloat:
    """rms_norm(Tensor input, SymInt[] normalized_shape, Tensor? weight=None, float? eps=None) -> Tensor"""

    # Default eps value if not provided
    if eps is None:
        eps = torch.finfo(torch.float).eps  # Observed from decomp

    # Calculate axis: the first normalization dimension
    # For normalized_shape with D dimensions, normalize over last D dimensions
    # Since ONNX RMSNormalization supports negative axis values, we use -len(normalized_shape)
    # which correctly maps to the first axis of the normalized dimensions
    normalized_dims = len(normalized_shape)
    axis = -normalized_dims

    # Create weight tensor if not provided
    if weight is None:
        weight = op23.ConstantOfShape(
            op23.Shape(input), value=ir.tensor([1], dtype=input.dtype)
        )

    return op23.RMSNormalization(input, weight, axis=axis, epsilon=eps)

