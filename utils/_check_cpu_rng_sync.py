from typing import Any

def _check_cpu_rng_sync(
    generator: torch.Generator, group: dist.ProcessGroup
) -> tuple[dict[Any, set], str]:
    # seed is returned as uint64_t from C impl, so may not fit in torch int64 tensor directly.
    state_tensor = generator.get_state()
    all_state_tensors = [torch.empty_like(state_tensor) for _ in range(group.size())]
    torch.distributed.all_gather(all_state_tensors, state_tensor)
    state_ranks = defaultdict(set)
    for rank, state_tensor in enumerate(all_state_tensors):
        # Summarize the state vector of the CPU rng.
        # The properties that matter most are (1) its different if there is a state difference, (2) its printable
        # (see desync table- not viable to print whole state vector of size 5k)
        state_ranks[torch.hash_tensor(state_tensor).item()].add(rank)
    return state_ranks, "Generator state hash"

