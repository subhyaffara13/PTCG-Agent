
def dump_cache_stats() -> None:
    if not log.isEnabledFor(logging.INFO):
        return

    import io

    out = io.StringIO()

    if not cache_stats._stats:
        print(" None", file=out)
    else:
        print(file=out)
        for k, v in sorted(cache_stats._stats.items()):
            print(f"  {k}: {v}", file=out)

    log.info("Cache Metrics:%s", out.getvalue())


def dump_cache_stats() -> None:
    log.info("FakeTensor cache stats:")
    log.info("  cache_hits: %s", FakeTensorMode.cache_hits)
    log.info("  cache_misses: %s", FakeTensorMode.cache_misses)
    bypasses = FakeTensorMode.cache_bypasses
    if bypasses:
        log.info("  cache_bypasses:")
        width = max(len(k) for k in bypasses)
        for k, v in sorted(bypasses.items(), key=lambda i: -i[1]):
            log.info("    %-*s %s", width + 1, f"{k}:", v)

