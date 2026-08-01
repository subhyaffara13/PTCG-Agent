
def quat_multiply_by_vec(quat: torch.Tensor, vec: torch.Tensor) -> torch.Tensor:
    """Multiply a quaternion by a pure-vector quaternion."""
    mat = _get_quat("_QUAT_MULTIPLY_BY_VEC", dtype=quat.dtype, device=quat.device)
    reshaped_mat = mat.view((1,) * len(quat.shape[:-1]) + mat.shape)
    return torch.sum(reshaped_mat * quat[..., :, None, None] * vec[..., None, :, None], dim=(-3, -2))

