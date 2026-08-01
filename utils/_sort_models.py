
def _sort_models(
    all_models: List[Dict[str, Any]],
    sort_by: Optional[str],
    sort_order: str = "asc",
) -> List[Dict[str, Any]]:
    """
    Sort models by the specified field and order.

    Args:
        all_models: List of models to sort
        sort_by: Field to sort by (model_name, created_at, updated_at, costs, status)
        sort_order: Sort order (asc or desc)

    Returns:
        Sorted list of models
    """
    if not sort_by or sort_by not in [
        "model_name",
        "created_at",
        "updated_at",
        "costs",
        "status",
    ]:
        return all_models

    reverse = sort_order.lower() == "desc"

    def get_sort_key(model: Dict[str, Any]) -> Any:
        model_info = model.get("model_info", {})

        if sort_by == "model_name":
            # Team BYOK models persist an internal `model_name` (e.g.
            # `model_name_{team_id}_{uuid}`) and expose the user-facing
            # name via `model_info.team_public_model_name` — same as the
            # UI's getDisplayModelName. Sort by the displayed name so
            # BYOK rows interleave alphabetically with non-BYOK rows
            # instead of clumping at the end on their opaque IDs.
            team_public_model_name = model_info.get("team_public_model_name")
            if team_public_model_name:
                return str(team_public_model_name).lower()
            return model.get("model_name", "").lower()

        elif sort_by == "created_at":
            created_at = model_info.get("created_at")
            normalized_dt = _normalize_datetime_for_sorting(created_at)
            if normalized_dt is None:
                # Put None values at the end for asc, at the start for desc
                return (
                    datetime.max.replace(tzinfo=timezone.utc)
                    if not reverse
                    else datetime.min.replace(tzinfo=timezone.utc)
                )
            return normalized_dt

        elif sort_by == "updated_at":
            updated_at = model_info.get("updated_at")
            normalized_dt = _normalize_datetime_for_sorting(updated_at)
            if normalized_dt is None:
                return (
                    datetime.max.replace(tzinfo=timezone.utc)
                    if not reverse
                    else datetime.min.replace(tzinfo=timezone.utc)
                )
            return normalized_dt

        elif sort_by == "costs":
            input_cost = model_info.get("input_cost_per_token", 0) or 0
            output_cost = model_info.get("output_cost_per_token", 0) or 0
            total_cost = input_cost + output_cost
            # Put 0 or None costs at the end for asc, at the start for desc
            if total_cost == 0:
                return float("inf") if not reverse else float("-inf")
            return total_cost

        elif sort_by == "status":
            # False (config) comes before True (db) for asc
            db_model = model_info.get("db_model", False)
            return db_model

        return None

    try:
        sorted_models = sorted(all_models, key=get_sort_key, reverse=reverse)
        return sorted_models
    except Exception as e:
        verbose_proxy_logger.exception(f"Error sorting models by {sort_by}: {str(e)}")
        return all_models

