from typing import Any, Dict, List

def _strip_client_pricing_overrides(data: Dict[str, Any]) -> None:
    """Drop pricing overrides from the request body and any metadata variant.

    Skipped only when the calling key/team carries
    ``allow_client_pricing_override: True`` in its metadata. Emits a
    ``debug``-level log line naming the dropped fields so operators can
    trace why a client-supplied pricing override stopped being applied
    (otherwise the strip is invisible from the caller's perspective).
    """
    stripped: List[str] = []
    for field in _CLIENT_PRICING_CONTROL_FIELDS:
        if field in data:
            stripped.append(field)
            data.pop(field, None)
    for metadata_key in ("metadata", "litellm_metadata"):
        metadata = data.get(metadata_key)
        if not isinstance(metadata, dict):
            continue
        for field in _CLIENT_PRICING_METADATA_FIELDS:
            if field in metadata:
                stripped.append(f"{metadata_key}.{field}")
                metadata.pop(field, None)
    if stripped:
        verbose_proxy_logger.debug(
            "Stripped client-supplied pricing fields from request body: %s. "
            "Set `allow_client_pricing_override: true` on the key or team "
            "metadata to keep these values.",
            ", ".join(stripped),
        )

