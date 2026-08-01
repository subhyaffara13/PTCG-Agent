
def _all_gather_keys(
    local_dict: dict[str, Any], group: dist.ProcessGroup | None = None
) -> set[str]:
    """Gathers all keys, and returns them sorted."""
    keys = list(local_dict.keys())
    gathered_keys: list[list[str]] = [None] * dist.get_world_size(group)  # type: ignore[list-item]

    dist.all_gather_object(gathered_keys, keys, group=group)
    return set(itertools.chain.from_iterable(gathered_keys))

