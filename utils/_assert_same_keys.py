
def _assert_same_keys(
    state_dict: dict[str, Any], process_group: dist.ProcessGroup | None = None
) -> None:
    """
    Asserts that all ranks have the same keys in their state dict.
    This is a collective call which requires all ranks in ``process_group`` to
    join. It will also induce cross-rank communication and block CPU.
    """

    if dist.get_world_size(process_group) == 1:
        return

    all_keys = _all_gather_keys(state_dict, process_group)
    my_keys = set(state_dict.keys())
    diff = all_keys - my_keys
    if len(diff) > 0:
        raise AssertionError(
            f"Key(s) present in other ranks but not this one, difference: {diff}"
        )

