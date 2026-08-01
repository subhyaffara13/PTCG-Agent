
def _build_managed_file_object(
    snapshot: Optional[Dict[str, Any]], managed_id: str
) -> Optional[OpenAIFileObject]:
    """Build an ``OpenAIFileObject`` (with the managed ID swapped in) from an
    upstream file response so the DB-served list returns the same metadata as a
    direct file GET.  Returns ``None`` when no usable snapshot is available, in
    which case the row is stored without metadata (previous behaviour)."""
    if not snapshot:
        return None
    try:
        return OpenAIFileObject(**{**snapshot, "id": managed_id})
    except Exception:
        verbose_proxy_logger.debug(
            "managed_id_rewriter: file object snapshot incomplete; "
            "storing file row without list metadata",
            exc_info=True,
        )
        return None

