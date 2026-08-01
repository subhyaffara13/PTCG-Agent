
def _build_aggregated_sql_query(
    *,
    table_name: str,
    entity_id_field: str,
    entity_id: Optional[Union[str, List[str]]],
    start_date: str,
    end_date: str,
    model: Optional[str],
    api_key: Optional[str],
    exclude_entity_ids: Optional[List[str]] = None,
    timezone_offset_minutes: Optional[int] = None,
) -> Tuple[str, List[Any]]:
    """Build a parameterized SQL GROUP BY query for aggregated daily activity.

    Groups by (date, api_key, model, model_group, custom_llm_provider,
    mcp_namespaced_tool_name, endpoint) with SUMs on all metric columns.
    The entity_id column is intentionally omitted from GROUP BY to collapse
    rows across entities — this is where the biggest row reduction comes from.

    Returns:
        Tuple of (sql_query, params_list) ready for prisma_client.db.query_raw().
    """
    pg_table = _PRISMA_TO_PG_TABLE.get(table_name)
    if pg_table is None:
        raise ValueError(f"Unknown table name: {table_name}")

    adjusted_start, adjusted_end = _adjust_dates_for_timezone(
        start_date, end_date, timezone_offset_minutes
    )

    sql_conditions: List[str] = []
    sql_params: List[Any] = []
    p = 1  # parameter index (1-based for PostgreSQL $N placeholders)

    # Date range (always present)
    sql_conditions.append(f"date >= ${p}")
    sql_params.append(adjusted_start)
    p += 1

    sql_conditions.append(f"date <= ${p}")
    sql_params.append(adjusted_end)
    p += 1

    # Optional entity filter
    if entity_id is not None:
        if isinstance(entity_id, list):
            placeholders = ", ".join(f"${p + i}" for i in range(len(entity_id)))
            sql_conditions.append(f'"{entity_id_field}" IN ({placeholders})')
            sql_params.extend(entity_id)
            p += len(entity_id)
        else:
            sql_conditions.append(f'"{entity_id_field}" = ${p}')
            sql_params.append(entity_id)
            p += 1

    # Exclude specific entities
    if exclude_entity_ids:
        placeholders = ", ".join(f"${p + i}" for i in range(len(exclude_entity_ids)))
        sql_conditions.append(f'"{entity_id_field}" NOT IN ({placeholders})')
        sql_params.extend(exclude_entity_ids)
        p += len(exclude_entity_ids)

    # Optional model filter
    if model:
        sql_conditions.append(f"model = ${p}")
        sql_params.append(model)
        p += 1

    # Optional api_key filter
    if api_key:
        sql_conditions.append(f"api_key = ${p}")
        sql_params.append(api_key)
        p += 1

    where_clause = " AND ".join(sql_conditions)

    # Postgres computes every rollup level the response needs — per-date
    # totals, per-(date, model), per-(date, model, api_key), per-provider,
    # etc. — in a single pass via GROUPING SETS. The GROUPING() bitmask
    # encodes which level a row belongs to so Python can dispatch rows
    # straight into their buckets without re-summing. The leaf grouping
    # is omitted on purpose: nothing in the response shape needs it once
    # all the rollups are present.
    sql_query = f"""
        SELECT
            date,
            api_key,
            model,
            model_group,
            custom_llm_provider,
            mcp_namespaced_tool_name,
            endpoint,
            GROUPING(date, api_key, model, model_group,
                     custom_llm_provider, mcp_namespaced_tool_name,
                     endpoint) AS group_level,
            SUM(spend)::float AS spend,
            SUM(prompt_tokens)::bigint AS prompt_tokens,
            SUM(completion_tokens)::bigint AS completion_tokens,
            SUM(cache_read_input_tokens)::bigint AS cache_read_input_tokens,
            SUM(cache_creation_input_tokens)::bigint AS cache_creation_input_tokens,
            SUM(api_requests)::bigint AS api_requests,
            SUM(successful_requests)::bigint AS successful_requests,
            SUM(failed_requests)::bigint AS failed_requests
        FROM "{pg_table}"
        WHERE {where_clause}
        GROUP BY GROUPING SETS (
            (date),
            (date, api_key),
            (date, model),
            (date, model, api_key),
            (date, model_group),
            (date, model_group, api_key),
            (date, custom_llm_provider),
            (date, custom_llm_provider, api_key),
            (date, mcp_namespaced_tool_name),
            (date, mcp_namespaced_tool_name, api_key),
            (date, endpoint),
            (date, endpoint, api_key),
            ()
        )
    """

    return sql_query, sql_params

