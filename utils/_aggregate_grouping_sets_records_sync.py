
def _aggregate_grouping_sets_records_sync(
    *,
    records: List[Any],
    api_key_metadata: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """Build the response from rollup rows produced by the GROUPING SETS query.

    Each row carries a `group_level` bitmask (from Postgres GROUPING()) that
    identifies which rollup level it belongs to. We dispatch the row's
    pre-aggregated metrics straight into the matching bucket — no per-row
    summing in Python and no nested update_metrics calls.
    """
    total_metrics = SpendMetrics()
    grouped_data: Dict[str, Dict[str, Any]] = {}

    def ensure_date(date_str: str) -> Dict[str, Any]:
        bucket = grouped_data.get(date_str)
        if bucket is None:
            bucket = {"metrics": SpendMetrics(), "breakdown": BreakdownMetrics()}
            grouped_data[date_str] = bucket
        return bucket

    def assign_metric_with_metadata(
        target: Dict[str, MetricWithMetadata], key: str, metrics: SpendMetrics
    ) -> None:
        existing = target.get(key)
        if existing is None:
            target[key] = MetricWithMetadata(metrics=metrics, metadata={})
        else:
            existing.metrics = metrics

    def assign_api_key_breakdown(
        target: Dict[str, MetricWithMetadata],
        parent_key: str,
        api_key: str,
        metrics: SpendMetrics,
    ) -> None:
        parent = target.get(parent_key)
        if parent is None:
            parent = MetricWithMetadata(metrics=SpendMetrics(), metadata={})
            target[parent_key] = parent
        parent.api_key_breakdown[api_key] = KeyMetricWithMetadata(
            metrics=metrics, metadata=_key_metadata(api_key_metadata, api_key)
        )

    for record in records:
        level = record.group_level
        metrics = _record_to_spend_metrics(record)

        if level == _GROUP_GRAND_TOTAL:
            total_metrics = metrics
            continue

        if level == _GROUP_DATE:
            ensure_date(record.date)["metrics"] = metrics
            continue

        breakdown = ensure_date(record.date)["breakdown"]

        if level == _GROUP_DATE_API_KEY:
            if record.api_key:
                breakdown.api_keys[record.api_key] = KeyMetricWithMetadata(
                    metrics=metrics,
                    metadata=_key_metadata(api_key_metadata, record.api_key),
                )
        elif level == _GROUP_DATE_MODEL:
            if record.model:
                assign_metric_with_metadata(breakdown.models, record.model, metrics)
        elif level == _GROUP_DATE_MODEL_API_KEY:
            if record.model and record.api_key:
                assign_api_key_breakdown(
                    breakdown.models, record.model, record.api_key, metrics
                )
        elif level == _GROUP_DATE_MODEL_GROUP:
            if record.model_group:
                assign_metric_with_metadata(
                    breakdown.model_groups, record.model_group, metrics
                )
        elif level == _GROUP_DATE_MODEL_GROUP_API_KEY:
            if record.model_group and record.api_key:
                assign_api_key_breakdown(
                    breakdown.model_groups,
                    record.model_group,
                    record.api_key,
                    metrics,
                )
        elif level == _GROUP_DATE_PROVIDER:
            provider = record.custom_llm_provider or "unknown"
            assign_metric_with_metadata(breakdown.providers, provider, metrics)
        elif level == _GROUP_DATE_PROVIDER_API_KEY:
            if record.api_key:
                provider = record.custom_llm_provider or "unknown"
                assign_api_key_breakdown(
                    breakdown.providers, provider, record.api_key, metrics
                )
        elif level == _GROUP_DATE_MCP:
            if record.mcp_namespaced_tool_name:
                assign_metric_with_metadata(
                    breakdown.mcp_servers, record.mcp_namespaced_tool_name, metrics
                )
        elif level == _GROUP_DATE_MCP_API_KEY:
            if record.mcp_namespaced_tool_name and record.api_key:
                assign_api_key_breakdown(
                    breakdown.mcp_servers,
                    record.mcp_namespaced_tool_name,
                    record.api_key,
                    metrics,
                )
        elif level == _GROUP_DATE_ENDPOINT:
            if record.endpoint:
                assign_metric_with_metadata(
                    breakdown.endpoints, record.endpoint, metrics
                )
        elif level == _GROUP_DATE_ENDPOINT_API_KEY:
            if record.endpoint and record.api_key:
                assign_api_key_breakdown(
                    breakdown.endpoints, record.endpoint, record.api_key, metrics
                )

    results = [
        DailySpendData(
            date=datetime.strptime(date_str, "%Y-%m-%d").date(),
            metrics=data["metrics"],
            breakdown=data["breakdown"],
        )
        for date_str, data in grouped_data.items()
    ]
    results.sort(key=lambda x: x.date, reverse=True)

    return {"results": results, "totals": total_metrics}

