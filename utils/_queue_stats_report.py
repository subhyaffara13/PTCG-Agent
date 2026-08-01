
def _queue_stats_report() -> None:
    stats = _queue_stats
    if stats.pool_count == 0:
        return

    timing = stats.timing
    timing.sort()

    log.info("AsyncCompile Metrics:")
    log.info("  Pools %s", stats.pool_count)
    log.info(
        "  Items %d enqueued / %d dequeued", stats.enqueue_count, stats.dequeue_count
    )
    log.info("  Max Queue Depth: %d", stats.max_queue_depth)
    n = len(timing)
    if n > 0:
        log.info("  Longest queue time: %0.2fs", timing[-1])
        log.info("  P50: %0.2fs", timing[n // 2])
        if n >= 20:
            log.info("  P95: %0.2fs", timing[n * 95 // 100])

