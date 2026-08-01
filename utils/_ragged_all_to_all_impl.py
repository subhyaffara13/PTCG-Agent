
def _ragged_all_to_all_impl(*args, **kwargs):
  raise RuntimeError("ragged_all_to_all must be used within a mapped context"
                     " like vmap or shard_map.")

