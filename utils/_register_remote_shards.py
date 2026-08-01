
def _register_remote_shards(
    sharded_tensor_id: int, rrefs: list[rpc.RRef[Shard]], rpc_rank: int
):
    with _sharded_tensor_lock:
        if sharded_tensor_id not in _sharded_tensor_map:
            raise RuntimeError(
                f"Could not find sharded_tensor_id: {sharded_tensor_id} in map: {_sharded_tensor_map.keys()}"
            )

        sharded_tensor = _sharded_tensor_map[sharded_tensor_id]()
        if sharded_tensor is None:
            raise RuntimeError("ShardedTensor weakref has been deallocated")
        else:
            sharded_tensor._register_remote_shards(rrefs, rpc_rank)

