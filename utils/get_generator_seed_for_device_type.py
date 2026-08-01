
def get_generator_seed_for_device_type(device_type: str):
    """
    Gets the generator seed for a specific device type, handling LocalTensor mode appropriately.

    Args:
        device_type: The device type (e.g., "cuda", "cpu")

    Returns:
        If in LocalTensor mode with per-rank RNG states:
            - Returns int if all ranks have the same seed
            - Returns SymInt(LocalIntNode) if ranks have different seeds
        Otherwise:
              - Returns int seed from the device's RNG state
    """
    if lm := enabled_local_tensor_mode():
        if len(lm._per_rank_rng_states) == 0:
            device_module = torch.get_device_module(device_type)
            return device_module.get_rng_state()[:8].view(torch.int64).item()
        device_module = torch.get_device_module(device_type)

        original_state = _get_rng_state()

        rank_seeds = {}
        try:
            for rank in sorted(lm.ranks):
                _set_rng_state(*lm._per_rank_rng_states[rank])
                rank_seeds[rank] = int(
                    device_module.get_rng_state()[:8].view(torch.int64).item()
                )
        finally:
            # restore original state
            _set_rng_state(*original_state)

        unique_seeds = set(rank_seeds.values())
        if len(unique_seeds) == 1:
            return next(iter(unique_seeds))
        local_int_node = LocalIntNode(rank_seeds)
        return torch.SymInt(local_int_node)
    else:
        device_module = torch.get_device_module(device_type)
        return device_module.get_rng_state()[:8].view(torch.int64).item()

