
def _push_candidate(
    output: ArrayIndexType,
    sizes: Dict[str, Any],
    remaining: Dict[ArrayIndexType, int],
    footprints: Dict[ArrayIndexType, int],
    dim_ref_counts: Dict[int, Set[str]],
    k1: ArrayIndexType,
    k2s: List[ArrayIndexType],
    queue: List[GreedyContractionType],
    push_all: bool,
    cost_fn: Any,
) -> None:
    candidates = (_get_candidate(output, sizes, remaining, footprints, dim_ref_counts, k1, k2, cost_fn) for k2 in k2s)
    if push_all:
        # want to do this if we e.g. are using a custom 'choose_fn'
        for candidate in candidates:
            heapq.heappush(queue, candidate)
    else:
        heapq.heappush(queue, min(candidates))

