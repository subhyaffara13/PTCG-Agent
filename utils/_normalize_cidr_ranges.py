
def _normalize_cidr_ranges(configured_ranges: Any, *, setting_name: str) -> List[str]:
    if not configured_ranges:
        return []
    if isinstance(configured_ranges, str):
        return [
            raw_range.strip()
            for raw_range in configured_ranges.split(",")
            if raw_range.strip()
        ]
    if isinstance(configured_ranges, (list, tuple, set)):
        return [
            str(raw_range).strip()
            for raw_range in configured_ranges
            if str(raw_range).strip()
        ]
    verbose_proxy_logger.warning(
        "Invalid %s value: expected a list of CIDR ranges, got %s",
        setting_name,
        type(configured_ranges).__name__,
    )
    return []

