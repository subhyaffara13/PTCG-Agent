
def _should_use_pickle(t: torch.Tensor) -> bool:
    return _is_tensor_subclass(t) and not _is_fake_tensor(t)

