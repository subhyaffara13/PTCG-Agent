
def record_has_frozen_params(gm: torch.fx.GraphModule) -> None:
    """
    Mark the gm as having frozen params.
    """
    gm._has_frozen_params = True  # type: ignore[assignment]

