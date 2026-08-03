from typing import Any, Dict, Optional

def update_breakdown_metrics(
    breakdown: BreakdownMetrics,
    record: Any,
    model_metadata: Dict[str, Dict[str, Any]],
    provider_metadata: Dict[str, Dict[str, Any]],
    api_key_metadata: Dict[str, Dict[str, Any]],
    entity_id_field: Optional[str] = None,
    entity_metadata_field: Optional[Dict[str, dict]] = None,
) -> BreakdownMetrics:
    """Updates breakdown metrics for a single record using the existing update_metrics function"""

    # Update model breakdown
    if record.model and record.model not in breakdown.models:
        breakdown.models[record.model] = MetricWithMetadata(
            metrics=SpendMetrics(),
            metadata=model_metadata.get(
                record.model, {}
            ),  # Add any model-specific metadata here
        )
    if record.model:
        breakdown.models[record.model].metrics = update_metrics(
            breakdown.models[record.model].metrics, record
        )

        # Update API key breakdown for this model
        if record.api_key not in breakdown.models[record.model].api_key_breakdown:
            breakdown.models[record.model].api_key_breakdown[record.api_key] = (
                KeyMetricWithMetadata(
                    metrics=SpendMetrics(),
                    metadata=KeyMetadata(
                        key_alias=api_key_metadata.get(record.api_key, {}).get(
                            "key_alias", None
                        ),
                        team_id=api_key_metadata.get(record.api_key, {}).get(
                            "team_id", None
                        ),
                    ),
                )
            )
        breakdown.models[record.model].api_key_breakdown[record.api_key].metrics = (
            update_metrics(
                breakdown.models[record.model]
                .api_key_breakdown[record.api_key]
                .metrics,
                record,
            )
        )

    # Update model group breakdown
    if record.model_group and record.model_group not in breakdown.model_groups:
        breakdown.model_groups[record.model_group] = MetricWithMetadata(
            metrics=SpendMetrics(),
            metadata=model_metadata.get(record.model_group, {}),
        )
    if record.model_group:
        breakdown.model_groups[record.model_group].metrics = update_metrics(
            breakdown.model_groups[record.model_group].metrics, record
        )

        # Update API key breakdown for this model
        if (
            record.api_key
            not in breakdown.model_groups[record.model_group].api_key_breakdown
        ):
            breakdown.model_groups[record.model_group].api_key_breakdown[
                record.api_key
            ] = KeyMetricWithMetadata(
                metrics=SpendMetrics(),
                metadata=KeyMetadata(
                    key_alias=api_key_metadata.get(record.api_key, {}).get(
                        "key_alias", None
                    ),
                    team_id=api_key_metadata.get(record.api_key, {}).get(
                        "team_id", None
                    ),
                ),
            )
        breakdown.model_groups[record.model_group].api_key_breakdown[
            record.api_key
        ].metrics = update_metrics(
            breakdown.model_groups[record.model_group]
            .api_key_breakdown[record.api_key]
            .metrics,
            record,
        )

    if record.mcp_namespaced_tool_name:
        if record.mcp_namespaced_tool_name not in breakdown.mcp_servers:
            breakdown.mcp_servers[record.mcp_namespaced_tool_name] = MetricWithMetadata(
                metrics=SpendMetrics(),
                metadata={},
            )
        breakdown.mcp_servers[record.mcp_namespaced_tool_name].metrics = update_metrics(
            breakdown.mcp_servers[record.mcp_namespaced_tool_name].metrics, record
        )

        # Update API key breakdown for this MCP server
        if (
            record.api_key
            not in breakdown.mcp_servers[
                record.mcp_namespaced_tool_name
            ].api_key_breakdown
        ):
            breakdown.mcp_servers[record.mcp_namespaced_tool_name].api_key_breakdown[
                record.api_key
            ] = KeyMetricWithMetadata(
                metrics=SpendMetrics(),
                metadata=KeyMetadata(
                    key_alias=api_key_metadata.get(record.api_key, {}).get(
                        "key_alias", None
                    ),
                    team_id=api_key_metadata.get(record.api_key, {}).get(
                        "team_id", None
                    ),
                ),
            )

        breakdown.mcp_servers[record.mcp_namespaced_tool_name].api_key_breakdown[
            record.api_key
        ].metrics = update_metrics(
            breakdown.mcp_servers[record.mcp_namespaced_tool_name]
            .api_key_breakdown[record.api_key]
            .metrics,
            record,
        )

    # Update provider breakdown
    provider = record.custom_llm_provider or "unknown"
    if provider not in breakdown.providers:
        breakdown.providers[provider] = MetricWithMetadata(
            metrics=SpendMetrics(),
            metadata=provider_metadata.get(
                provider, {}
            ),  # Add any provider-specific metadata here
        )
    breakdown.providers[provider].metrics = update_metrics(
        breakdown.providers[provider].metrics, record
    )

    # Update API key breakdown for this provider
    if record.api_key not in breakdown.providers[provider].api_key_breakdown:
        breakdown.providers[provider].api_key_breakdown[record.api_key] = (
            KeyMetricWithMetadata(
                metrics=SpendMetrics(),
                metadata=KeyMetadata(
                    key_alias=api_key_metadata.get(record.api_key, {}).get(
                        "key_alias", None
                    ),
                    team_id=api_key_metadata.get(record.api_key, {}).get(
                        "team_id", None
                    ),
                ),
            )
        )
    breakdown.providers[provider].api_key_breakdown[record.api_key].metrics = (
        update_metrics(
            breakdown.providers[provider].api_key_breakdown[record.api_key].metrics,
            record,
        )
    )

    # Update endpoint breakdown
    if record.endpoint:
        if record.endpoint not in breakdown.endpoints:
            breakdown.endpoints[record.endpoint] = MetricWithMetadata(
                metrics=SpendMetrics(),
                metadata={},
            )
        breakdown.endpoints[record.endpoint].metrics = update_metrics(
            breakdown.endpoints[record.endpoint].metrics, record
        )

        # Update API key breakdown for this endpoint
        if record.api_key not in breakdown.endpoints[record.endpoint].api_key_breakdown:
            breakdown.endpoints[record.endpoint].api_key_breakdown[record.api_key] = (
                KeyMetricWithMetadata(
                    metrics=SpendMetrics(),
                    metadata=KeyMetadata(
                        key_alias=api_key_metadata.get(record.api_key, {}).get(
                            "key_alias", None
                        ),
                        team_id=api_key_metadata.get(record.api_key, {}).get(
                            "team_id", None
                        ),
                    ),
                )
            )
        breakdown.endpoints[record.endpoint].api_key_breakdown[
            record.api_key
        ].metrics = update_metrics(
            breakdown.endpoints[record.endpoint]
            .api_key_breakdown[record.api_key]
            .metrics,
            record,
        )

    # Update api key breakdown
    if record.api_key not in breakdown.api_keys:
        breakdown.api_keys[record.api_key] = KeyMetricWithMetadata(
            metrics=SpendMetrics(),
            metadata=KeyMetadata(
                key_alias=api_key_metadata.get(record.api_key, {}).get(
                    "key_alias", None
                ),
                team_id=api_key_metadata.get(record.api_key, {}).get("team_id", None),
            ),  # Add any api_key-specific metadata here
        )
    breakdown.api_keys[record.api_key].metrics = update_metrics(
        breakdown.api_keys[record.api_key].metrics, record
    )

    # Update entity-specific metrics if entity_id_field is provided
    if entity_id_field:
        entity_value = getattr(record, entity_id_field, None)
        entity_value = (
            entity_value if entity_value else "Unassigned"
        )  # allow for null entity_id_field
        if entity_value not in breakdown.entities:
            breakdown.entities[entity_value] = MetricWithMetadata(
                metrics=SpendMetrics(),
                metadata=(
                    entity_metadata_field.get(entity_value, {})
                    if entity_metadata_field
                    else {}
                ),
            )
        breakdown.entities[entity_value].metrics = update_metrics(
            breakdown.entities[entity_value].metrics, record
        )

        # Update API key breakdown for this entity
        if record.api_key not in breakdown.entities[entity_value].api_key_breakdown:
            breakdown.entities[entity_value].api_key_breakdown[record.api_key] = (
                KeyMetricWithMetadata(
                    metrics=SpendMetrics(),
                    metadata=KeyMetadata(
                        key_alias=api_key_metadata.get(record.api_key, {}).get(
                            "key_alias", None
                        ),
                        team_id=api_key_metadata.get(record.api_key, {}).get(
                            "team_id", None
                        ),
                    ),
                )
            )
        breakdown.entities[entity_value].api_key_breakdown[record.api_key].metrics = (
            update_metrics(
                breakdown.entities[entity_value]
                .api_key_breakdown[record.api_key]
                .metrics,
                record,
            )
        )

    return breakdown

