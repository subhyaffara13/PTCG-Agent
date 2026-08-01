
def numpy_take(x: Tensor, ind: Tensor, ind_inv: Tensor, dim: int) -> Tensor:
    device = x.device
    x = to_numpy(x)
    ind = to_numpy(ind)
    return torch.tensor(np.take_along_axis(x, ind, dim), device=device)

