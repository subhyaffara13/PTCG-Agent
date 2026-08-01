
def _checkerboard_mask(
    tensor: torch.Tensor, tensor_idx: int = 0, mask_shift: int = 0
) -> torch.Tensor:
    """Checkerboard mask that alternates in every dimension.

    Unlike flat-index % 2, which can be uniform along even-stride dimensions
    (causing all elements in a reduction group to get the same offset), the
    checkerboard uses sum-of-coordinates mod 2 so adjacent elements differ
    along every axis.

    Returns a flat bool tensor of shape (numel,).
    """
    if tensor.ndim == 0:
        return torch.tensor([(tensor_idx + mask_shift) % 2 == 0], device=tensor.device)
    coords = [torch.arange(s, device=tensor.device) for s in tensor.shape]
    grids = torch.meshgrid(*coords, indexing="ij")
    coord_sum = grids[0].clone()
    for g in grids[1:]:
        coord_sum += g
    return ((coord_sum + tensor_idx + mask_shift) % 2 == 0).flatten()

