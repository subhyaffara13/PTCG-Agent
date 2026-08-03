from typing import Any

def _sort_with_ref_region(
    index_to_rank: dict[int, int], regions: list[list[Any]]
) -> None:
    # sort topologically
    # we need to handle edge cases where some nodes have no dependencies
    # so first we map each node to its ranking
    ref_region = regions[0]
    sorted_indices = sorted(range(len(ref_region)), key=lambda i: index_to_rank[i])
    for region in regions:
        region[:] = [region[i] for i in sorted_indices]

