from typing import Any

def update_metrics(existing_metrics: SpendMetrics, record: Any) -> SpendMetrics:
    """Update metrics with new record data.

    Rollup rows can carry None for numeric fields when SUM() spans zero rows
    (e.g. a key with no spend), so coalesce to 0 before accumulating to avoid
    a TypeError. Mirrors the handling in ``_record_to_spend_metrics``.
    """
    prompt_tokens = record.prompt_tokens or 0
    completion_tokens = record.completion_tokens or 0
    existing_metrics.spend += record.spend or 0.0
    existing_metrics.prompt_tokens += prompt_tokens
    existing_metrics.completion_tokens += completion_tokens
    existing_metrics.total_tokens += prompt_tokens + completion_tokens
    existing_metrics.cache_read_input_tokens += record.cache_read_input_tokens or 0
    existing_metrics.cache_creation_input_tokens += (
        record.cache_creation_input_tokens or 0
    )
    existing_metrics.api_requests += record.api_requests or 0
    existing_metrics.successful_requests += record.successful_requests or 0
    existing_metrics.failed_requests += record.failed_requests or 0
    return existing_metrics

