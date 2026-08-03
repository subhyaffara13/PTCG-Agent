from typing import Any, Dict, List, Optional, Union

def _build_where_conditions(
    *,
    entity_id_field: str,
    entity_id: Optional[Union[str, List[str]]],
    start_date: str,
    end_date: str,
    model: Optional[str],
    api_key: Optional[Union[str, List[str]]],
    exclude_entity_ids: Optional[List[str]] = None,
    timezone_offset_minutes: Optional[int] = None,
) -> Dict[str, Any]:
    """Build prisma where clause for daily activity queries."""
    # Adjust dates for timezone if provided
    adjusted_start, adjusted_end = _adjust_dates_for_timezone(
        start_date, end_date, timezone_offset_minutes
    )

    where_conditions: Dict[str, Any] = {
        "date": {
            "gte": adjusted_start,
            "lte": adjusted_end,
        }
    }

    if model:
        where_conditions["model"] = model
    if api_key:
        if isinstance(api_key, list):
            where_conditions["api_key"] = {"in": api_key}
        else:
            where_conditions["api_key"] = api_key

    if entity_id is not None:
        if isinstance(entity_id, list):
            where_conditions[entity_id_field] = {"in": entity_id}
        else:
            where_conditions[entity_id_field] = {"equals": entity_id}

    if exclude_entity_ids:
        current = where_conditions.get(entity_id_field, {})
        if isinstance(current, str):
            current = {"equals": current}
        current["not"] = {"in": exclude_entity_ids}
        where_conditions[entity_id_field] = current

    return where_conditions

