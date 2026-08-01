
def _all_to_all_impl(*args, **kwargs):
  raise RuntimeError("all_to_all must be used within a mapped context"
                     " like vmap or shard_map.")

