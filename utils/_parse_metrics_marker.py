
def _parse_metrics_marker(
    marker: Optional[object],
) -> Optional[datetime]:
    """Parse metricsMarker from Mavvrik register response into a UTC datetime.

    Handles both formats Mavvrik may return:
    - Unix timestamp (int/float): e.g. 1749340800
    - ISO date string: e.g. "2026-06-09" or "2026-06-09T00:00:00Z"

    Returns None for falsy values (0, None, empty string) which indicate
    no data has been ingested yet.
    """
    if not marker:
        return None
    try:
        if isinstance(marker, (int, float)):
            return datetime.fromtimestamp(float(marker), tz=timezone.utc).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
        if isinstance(marker, str):
            marker = marker.strip()
            if not marker:
                return None
            # Try ISO date first (YYYY-MM-DD), then full ISO datetime
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S"):
                try:
                    return datetime.strptime(marker, fmt).replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
    except Exception:
        pass
    verbose_proxy_logger.warning(
        "Mavvrik FOCUS: could not parse metricsMarker %r — skipping catch-up", marker
    )
    return None

