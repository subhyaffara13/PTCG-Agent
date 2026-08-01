
def add_ephemeral_timeout_increase_for_distributed(time_saved_ns: int) -> int:
    """
    Ephemerally increases the NCCL timeout when compiling for a distributed job
    Returns amount of seconds increased
    """
    if not torch.distributed.is_available() or not torch.distributed.is_initialized():
        return 0

    increased_timeout_sec = int(time_saved_ns // 1e9)  # convert to seconds

    if config.is_fbcode():
        fudge_factor = torch._utils_internal.justknobs_getval_int(
            "pytorch/remote_cache:ephemeral_timeout_fudge_factor_percentage"
        )
        log.info(
            "Ephemeral NCCL timeout increase fudge factor %d and original increase value %d",
            fudge_factor,
            increased_timeout_sec,
        )
        increased_timeout_sec += int(increased_timeout_sec * fudge_factor / 100)

    log.info("Increasing NCCL timeout by %d", increased_timeout_sec)
    dist.distributed_c10d._add_ephemeral_timeout_for_all_pgs(
        timedelta(seconds=increased_timeout_sec)
    )
    return increased_timeout_sec

