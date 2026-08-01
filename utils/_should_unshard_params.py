
def _should_unshard_params(fsdp_state: _FSDPState) -> bool:
    return not (
        fsdp_state.sharding_strategy == ShardingStrategy.NO_SHARD
        and (_is_composable(fsdp_state) or fsdp_state._use_orig_params)
    )

