
def _resolve_metric_attribute_filter(
    attributes: Optional[OTELMetricAttributeFilter],
) -> Tuple[Optional[FrozenSet[str]], Optional[FrozenSet[str]]]:
    if attributes is None:
        return None, None
    include = attributes.include_list or None
    exclude = attributes.exclude_list or None
    if include and exclude:
        raise ValueError(
            "otel.attributes: include_list and exclude_list are mutually exclusive"
        )
    requested = include or exclude or []
    if TOKEN_TYPE_ATTRIBUTE in requested:
        raise ValueError(
            f"otel.attributes: {TOKEN_TYPE_ATTRIBUTE} is a structural token-usage "
            "discriminator and cannot be filtered"
        )
    unknown = sorted(
        name for name in requested if name not in VALID_METRIC_ATTRIBUTE_NAMES
    )
    if unknown:
        raise ValueError(
            f"otel.attributes: unknown attribute name(s) {unknown}. "
            f"Valid names: {sorted(VALID_METRIC_ATTRIBUTE_NAMES)}"
        )
    return (
        frozenset(include) if include else None,
        frozenset(exclude) if exclude else None,
    )

