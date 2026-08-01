
def _create_default_load_balancer(
    seq_length: int, world_size: int, device: str | torch.device
) -> _LoadBalancer | None:
    from ._attention import _cp_options

    if _cp_options.enable_load_balance:
        return _HeadTailLoadBalancer(seq_length, world_size, device)
    else:
        return None

