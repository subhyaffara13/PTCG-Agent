
def _get_state_dict_2d_layout(
    state_dict: STATE_DICT_TYPE,
) -> tuple[STATE_DICT_2D_LAYOUT, dist.ProcessGroup | None]:
    """
    Load the right TP slice of the optimizer state.

    This is not easy since the per-tensor slicing can't be inferred from checkpoint metadata.
    We take advantage of the model state_dict producing a sliced ST to figure out what we need to load.
    This is pretty fragile and it might be easier for FSDP to compute this info for us.
    Returns a dictionary where keys are the same of the state_dict and the value is a tuple of
    (offset, size) for the current rank TP slice.
    N.B. The state_dict *MUST* come from FSDP.sharded_state_dict.
    """
    specs: STATE_DICT_2D_LAYOUT = {}
    dp_pg: dist.ProcessGroup | None = None
    for key, value in state_dict.items():
        specs[key] = (None, value.size())
        if _is_nested_tensor(value):
            if not len(value.local_shards()) == 1:
                raise AssertionError("Cannot handle ST with multiple shards")
            if not isinstance(value, ShardedTensor):
                raise AssertionError("Can only handle nested ShardedTensor")
            shard = value.local_shards()[0]
            specs[key] = (
                shard.metadata.shard_offsets,
                shard.metadata.shard_sizes,
            )
            dp_pg = shard.tensor._process_group  # type: ignore[attr-defined]

    return (
        specs,
        dp_pg,
    )

