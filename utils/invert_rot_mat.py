
def invert_rot_mat(rot_mat: torch.Tensor) -> torch.Tensor:
    return rot_mat.transpose(-1, -2)

