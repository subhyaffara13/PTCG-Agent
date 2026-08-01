
def _create_process_group_wrapper(
    wrapped_pg: torch._C._distributed_c10d.Backend,
    store_prefix: str,
    store: Store,
    rank: int,
    world_size: int,
    timeout: timedelta = default_pg_timeout,
):
    if not _GLOO_AVAILABLE:
        raise AssertionError("ProcessGroupWrapper unsupported without GLOO backend.")

    # (whc) this appears to be just for the gloo backend? if so, `default_pg_timeout` is appropriate...

    # Create a separate prefix store for the helper process group.
    prefix = f"{PG_WRAPPER_STORE_PREFIX}:{store_prefix}"
    store = PrefixStore(prefix, store)
    helper_pg = ProcessGroupGloo(store, rank, world_size, timeout=timeout)
    # Wrap the underlying pg with ProcessGroupWrapper.
    wrapped_pg = _ProcessGroupWrapper(wrapped_pg, helper_pg)
    return wrapped_pg

