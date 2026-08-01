
def flex_cp_allgather_backward(
    grad_full_k: torch.Tensor,
    grad_full_v: torch.Tensor,
    seq_dim: int,
    pg_name: c10d.GroupName,
) -> tuple[torch.Tensor, torch.Tensor]:
    grad_k = funcol.reduce_scatter_tensor(grad_full_k, "sum", seq_dim, pg_name)
    if isinstance(grad_k, funcol.AsyncCollectiveTensor):
        grad_k = grad_k.wait()
    grad_v = funcol.reduce_scatter_tensor(grad_full_v, "sum", seq_dim, pg_name)
    if isinstance(grad_v, funcol.AsyncCollectiveTensor):
        grad_v = grad_v.wait()

    return grad_k, grad_v

