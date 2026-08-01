
def _all_gather_into_tensor_meta(shard, tag, rankset, group_size):
    return _make_all_gather_out_tensor(shard, group_size)

