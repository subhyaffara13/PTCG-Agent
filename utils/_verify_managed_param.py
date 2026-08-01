
def _verify_managed_param(name: str, param: nn.Parameter) -> None:
    """
    Verify if the parameter is accepted by fully_shard. The only restriction now
    is that the parameter cannot be a scalar tensor (param.numel == 0) since we
    need at least one dim to shard.
    """
    if len(param.shape) == 0:
        raise ValueError(
            "fully_shard doesn't support scalar parameters. "
            f"Change {name} to a 1D tensor with numel equal to 1."
        )

