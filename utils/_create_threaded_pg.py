
def _create_threaded_pg(prefix_store, rank, world_size, timeout):
    pg = ProcessLocalGroup(rank, world_size)
    # https://github.com/pytorch/pytorch/pull/103033 changed store based barrier to optional
    # When device mesh involves sub groups while store based barrier is not enabled in c10d,
    # even though threaded pg actual collectives are assumed to be single threaded,
    # different threads may be initializing different groups,
    # leading to race conditions.
    # For example, if we have a mesh of [[0, 1], [2, 3]], the sub groups
    # (dim 0 and 1) would be initialized in different threads independently.
    # In this case we can no longer rely on class or global variables
    # but have to rely on store based barrier to make sure each group
    # is ready separately before we can invoke collectives in any of the groups.

    # the prefix store is already per group so we pass an empty name here
    _store_based_barrier(rank, prefix_store, "", world_size, timeout)
    return pg

