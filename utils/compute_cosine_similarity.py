
def compute_cosine_similarity(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
    """
    Computes the cosine similarity between `x` and `y`.

    Args:
        x: Tensor or tuple of tensors
        y: Tensor or tuple of tensors

    Return:
        float or tuple of floats
    """
    # For convolutions, the shape of the quantized weight has one additional
    # dimension compared to the shape of the fp32 weight. Match the shapes
    # to enable cosine similarity comparison.
    x = x.reshape(1, -1)
    y = y.reshape(1, -1)
    return torch.nn.functional.cosine_similarity(x, y)

