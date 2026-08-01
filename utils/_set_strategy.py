
def _set_strategy(_strategy: str) -> None:
    if not is_available():
        raise ValueError(
            f"opt_einsum is not available, so setting `strategy` to {_strategy} will not be meaningful. "
            "torch.einsum will bypass path calculation and simply contract from left to right. "
            "Please install opt_einsum or unset `strategy`."
        )
    if not enabled:
        raise ValueError(
            f"opt_einsum is not enabled, so setting a `strategy` to {_strategy} will not be meaningful. "
            "torch.einsum will bypass path calculation and simply contract from left to right. "
            "Please set `enabled` to `True` as well or unset `strategy`."
        )
    if _strategy not in ["auto", "greedy", "optimal"]:
        raise ValueError(
            f"`strategy` must be one of the following: [auto, greedy, optimal] but is {_strategy}"
        )
    global strategy
    strategy = _strategy

