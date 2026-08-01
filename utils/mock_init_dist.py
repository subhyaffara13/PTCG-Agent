
def mock_init_dist(rank, world_size):
    # !!! WARNING !!!
    # Kids don't try this at home, this is a cute pile of hacks that
    # depends on a small mountain of c10d internals
    if dist.is_initialized():
        raise AssertionError("Expected dist to not be initialized")
    store = dist.HashStore()
    # Trick _store_based_barrier into believing everyone else already checked-in
    # Zero is the group index
    store.add(f"{c10d.STORE_BASED_BARRIER_PREFIX}:0", world_size - 1)
    dist.init_process_group(
        backend="mock_process_group",
        rank=rank,
        world_size=world_size,
        store=store,
        group_name="fake",
        timeout=timedelta(seconds=1),
    )

