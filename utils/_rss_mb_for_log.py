
def _rss_mb_for_log() -> str:
    rss_mb = _get_process_rss_mb()
    if rss_mb is None:
        return "unknown"
    return f"{rss_mb:.2f}"


def _rss_mb_for_log() -> str:
    rss_mb = _get_process_rss_mb()
    if rss_mb is None:
        return "unknown"
    return f"{rss_mb:.2f}"

