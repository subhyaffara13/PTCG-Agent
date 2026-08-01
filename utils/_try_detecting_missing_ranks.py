
def _try_detecting_missing_ranks(
    store,
    world_size: int,
    key_prefix: str,
    rank: int,
    rank_decoder: Callable[[int], str],
    trace_timeout: float,
) -> Iterable[str] | None:
    store.set(f"{key_prefix}{rank}{_TRACE}", "<val_ignored>")

    def _find_missing_ranks():
        missing_rank_info = set()
        ranks_missing = 0
        for i in range(1, world_size):
            # reduce noise, assuming in general 8 ranks per node
            # It is valuable to know that 1 or >1 nodes have timed-out.
            if ranks_missing >= _MAX_TRACE_MISSING_RANKS:
                break
            try:
                if ranks_missing == 0:
                    store.wait(
                        [f"{key_prefix}{i}{_TRACE}"], timedelta(seconds=trace_timeout)
                    )
                else:
                    # use a shortest timeout, some ranks have failed to check-in
                    store.wait([f"{key_prefix}{i}{_TRACE}"], timedelta(milliseconds=1))
            except DistStoreError:
                ranks_missing += 1
                missing_rank_info.add(rank_decoder(i))
        return missing_rank_info

    def _checkin():
        try:
            store.wait([f"{key_prefix}{_TRACING_GATE}"])
            return [f"[<check rank 0 ({rank_decoder(0)}) for missing rank info>]"]
        except DistStoreError:
            # in case rank0 is the source of the timeout, original exception will be raised
            return None

    if rank == 0:
        missing_rank_info = _find_missing_ranks()
        store.set(f"{key_prefix}{_TRACING_GATE}", "<val_ignored>")
        return missing_rank_info
    else:
        return _checkin()

