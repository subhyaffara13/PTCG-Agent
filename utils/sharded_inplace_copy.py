
def sharded_inplace_copy(types, args, kwargs, pg):
    # NOTE: inplace op don't need to rewrap
    kwargs = {} if kwargs is None else kwargs
    self_st = args[0]
    new_st = args[1]
    nonblocking = kwargs.get("non_blocking", False)
    for local_shard, new_shard in zip(self_st.local_shards(), new_st.local_shards()):
        if local_shard.metadata != new_shard.metadata:
            raise RuntimeError(
                "inplace copy can only happen between two ShardedTensor with same metadata!"
            )
    for local_shard, new_shard in zip(self_st.local_shards(), new_st.local_shards()):
        local_shard.tensor.copy_(new_shard.tensor, nonblocking)

    return self_st

