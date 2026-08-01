
def numpy_nonzero(x: Tensor) -> Tensor:
    x_np = to_numpy(x)
    res = np.stack(np.nonzero(x_np), axis=1)
    if res.shape[0] <= 1:
        raise RuntimeError("not supported")
    return torch.tensor(res, device=x.device)

