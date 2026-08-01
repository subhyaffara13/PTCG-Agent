
def _svd_aten(
    A: TensorLikeType, *, full_matrices: bool
) -> tuple[Tensor, Tensor, Tensor]:
    return torch.linalg.svd(A, full_matrices=full_matrices)

