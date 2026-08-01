
def _check_philox_rng_sync(
    generator: torch.Generator, group: dist.ProcessGroup
) -> tuple[dict[Any, set], str]:
    local_state = generator.get_state()
    all_states = [torch.empty_like(local_state) for _ in range(group.size())]
    torch.distributed.all_gather(all_states, local_state)
    seeds_offsets = [
        (state[:8].view(torch.uint64).item(), state[8:].view(torch.uint64).item())
        for state in all_states
    ]
    seed_offset_ranks = defaultdict(set)
    for rank, (seed, offset) in enumerate(seeds_offsets):
        seed_offset_ranks[(seed, offset)].add(rank)
    return seed_offset_ranks, "(Seed, Offset)"

