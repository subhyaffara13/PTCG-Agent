
def _check_rng_sync(generator: torch.Generator, group: dist.ProcessGroup) -> str | None:
    value_ranks, value_header = _check_rng_sync_internal(generator, group)
    log_str = None
    if len(value_ranks) > 1:
        log_str = f"Generator desync detected:\n{_desync_table_str(value_header, value_ranks)}"
        logger.error(log_str)
    return log_str

