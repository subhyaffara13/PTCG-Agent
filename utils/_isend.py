
def _isend(tensor: torch.Tensor, dst: int, tag: str, group_name):
    return torch.ops._c10d_functional.isend(tensor, dst, tag, group_name)

