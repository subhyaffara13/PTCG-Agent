
def has_frozen_params(gm: torch.fx.GraphModule) -> bool:
    """
    Return True if the gm has frozen parameters.
    """
    return getattr(gm, "_has_frozen_params", False)

