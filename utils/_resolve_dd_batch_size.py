import os

def _resolve_dd_batch_size() -> int:
    raw = os.getenv("DD_BATCH_SIZE")
    if raw is None:
        return DD_MAX_BATCH_SIZE
    try:
        value = int(raw)
    except ValueError:
        verbose_logger.warning(
            "Datadog: ignoring invalid DD_BATCH_SIZE=%r, using %s",
            raw,
            DD_MAX_BATCH_SIZE,
        )
        return DD_MAX_BATCH_SIZE
    return max(1, min(value, DD_MAX_BATCH_SIZE))

