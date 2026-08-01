
def maybe_set_is_frozen_param(t: torch.Tensor) -> None:
    """
    Mark the provided tensor as a frozen param if freezing is active.
    """
    if _freezing_active():
        t._is_frozen_param = True  # type: ignore[attr-defined]

