import copy

def sharded_deepcopy(args, kwargs, pg):
    # NOTE: we directly implement deepcopy magic method
    # instead of using the default tensor.__deepcopy__
    # and implement clone(). This is because the default
    # tensor deepcopy copies every attribute, but the
    # process_group in ShardedTensor cannot be deep copied.
    self_st = args[0]
    new_local_shards = copy.deepcopy(self_st.local_shards())
    new_metadata = copy.deepcopy(self_st.metadata())
    return new_local_shards, new_metadata

