
def create_meshgrid(
    height: int | torch.Tensor,
    width: int | torch.Tensor,
    normalized_coordinates: bool = False,
    device: torch.device | None = None,
    dtype: torch.dtype | None = None,
) -> torch.Tensor:
    """
    Copied from kornia library : kornia/kornia/utils/grid.py:26

    Generate a coordinate grid for an image.

    When the flag ``normalized_coordinates`` is set to True, the grid is
    normalized to be in the range :math:`[-1,1]` to be consistent with the pytorch
    function :py:func:`torch.nn.functional.grid_sample`.

    Args:
        height (`int`):
            The image height (rows).
        width (`int`):
            The image width (cols).
        normalized_coordinates (`bool`):
            Whether to normalize coordinates in the range :math:`[-1,1]` in order to be consistent with the
            PyTorch function :py:func:`torch.nn.functional.grid_sample`.
        device (`torch.device`):
            The device on which the grid will be generated.
        dtype (`torch.dtype`):
            The data type of the generated grid.

    Return:
        grid (`torch.Tensor` of shape `(1, height, width, 2)`):
            The grid tensor.

    Example:
        >>> create_meshgrid(2, 2)
        tensor([[[[-1., -1.],
                  [ 1., -1.]],
        <BLANKLINE>
                 [[-1.,  1.],
                  [ 1.,  1.]]]])

        >>> create_meshgrid(2, 2, normalized_coordinates=False)
        tensor([[[[0., 0.],
                  [1., 0.]],
        <BLANKLINE>
                 [[0., 1.],
                  [1., 1.]]]])

    """
    xs = torch.linspace(0, width - 1, width, device=device, dtype=dtype)
    ys = torch.linspace(0, height - 1, height, device=device, dtype=dtype)
    if normalized_coordinates:
        xs = (xs / (width - 1) - 0.5) * 2
        ys = (ys / (height - 1) - 0.5) * 2
    grid = torch.stack(torch.meshgrid(ys, xs, indexing="ij"), dim=-1)
    grid = grid.permute(1, 0, 2).unsqueeze(0)
    return grid

