
def _record_to_spend_metrics(record: Any) -> SpendMetrics:
    """Build a SpendMetrics directly from one already-aggregated rollup row.

    SUM() over zero rows is SQL NULL, so rollup rows (notably the grand-total
    row, which Postgres emits even on an empty match) can carry None values.
    """
    prompt_tokens = record.prompt_tokens or 0
    completion_tokens = record.completion_tokens or 0
    return SpendMetrics(
        spend=record.spend or 0.0,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=prompt_tokens + completion_tokens,
        cache_read_input_tokens=record.cache_read_input_tokens or 0,
        cache_creation_input_tokens=record.cache_creation_input_tokens or 0,
        api_requests=record.api_requests or 0,
        successful_requests=record.successful_requests or 0,
        failed_requests=record.failed_requests or 0,
    )

