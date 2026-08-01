
def numpy_cat(xs: Sequence[Tensor], dim: int) -> Tensor:
    if len(xs) == 0:
        raise AssertionError("xs must not be empty")
    if not all(x.device == xs[0].device for x in xs):
        raise AssertionError("All tensors must be on the same device")
    if not all(x.dtype == xs[0].dtype for x in xs):
        raise AssertionError("All tensors must have the same dtype")
    np_xs = [to_numpy(x) for x in xs]
    np_out = np.concatenate(np_xs, axis=dim)
    return torch.tensor(np_out, device=xs[0].device)

