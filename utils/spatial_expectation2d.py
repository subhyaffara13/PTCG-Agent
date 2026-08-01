
def spatial_expectation2d(input: torch.Tensor, normalized_coordinates: bool = True) -> torch.Tensor:
    r"""
    Copied from kornia library : kornia/geometry/subpix/dsnt.py:76
    Compute the expectation of coordinate values using spatial probabilities.

    The input heatmap is assumed to represent a valid spatial probability distribution,
    which can be achieved using :func:`~kornia.geometry.subpixel.spatial_softmax2d`.

    Args:
        input (`torch.Tensor` of shape `(batch_size, embed_dim, height, width)`):
            The input tensor representing dense spatial probabilities.
        normalized_coordinates (`bool`):
            Whether to return the coordinates normalized in the range of :math:`[-1, 1]`. Otherwise, it will return
            the coordinates in the range of the input shape.

    Returns:
        output (`torch.Tensor` of shape `(batch_size, embed_dim, 2)`)
            Expected value of the 2D coordinates. Output order of the coordinates is (x, y).

    Examples:
        >>> heatmaps = torch.tensor([[[
        ... [0., 0., 0.],
        ... [0., 0., 0.],
        ... [0., 1., 0.]]]])
        >>> spatial_expectation2d(heatmaps, False)
        tensor([[[1., 2.]]])

    """
    batch_size, embed_dim, height, width = input.shape

    # Create coordinates grid.
    grid = create_meshgrid(height, width, normalized_coordinates, input.device)
    grid = grid.to(input.dtype)

    pos_x = grid[..., 0].reshape(-1)
    pos_y = grid[..., 1].reshape(-1)

    input_flat = input.view(batch_size, embed_dim, -1)

    # Compute the expectation of the coordinates.
    expected_y = torch.sum(pos_y * input_flat, -1, keepdim=True)
    expected_x = torch.sum(pos_x * input_flat, -1, keepdim=True)

    output = torch.cat([expected_x, expected_y], -1)

    return output.view(batch_size, embed_dim, 2)

