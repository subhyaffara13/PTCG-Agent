
def numpy_view_copy(x: Tensor, shape: Sequence[int]) -> Tensor:
    return torch.tensor(np.copy(to_numpy(x).reshape(shape)), device=x.device)

