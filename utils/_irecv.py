
def _irecv(tensor: torch.Tensor, src: int, tag: str, group_name):
    return torch.ops._c10d_functional.irecv(tensor, src, tag, group_name)

