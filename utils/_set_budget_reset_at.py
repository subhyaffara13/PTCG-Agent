
def _set_budget_reset_at(data: UpdateTeamRequest, updated_kv: dict) -> None:
    """Set budget_reset_at in updated_kv if budget_duration is provided."""
    if data.budget_duration is not None:
        from litellm.proxy.common_utils.timezone_utils import get_budget_reset_time

        reset_at = get_budget_reset_time(budget_duration=data.budget_duration)
        updated_kv["budget_reset_at"] = reset_at
    elif "budget_duration" in updated_kv and updated_kv["budget_duration"] is None:
        updated_kv["budget_reset_at"] = None

    if data.budget_limits is not None and len(data.budget_limits) > 0:
        from litellm.proxy.common_utils.timezone_utils import get_budget_reset_time

        initialized_windows = []
        for window in data.budget_limits:
            w = window if isinstance(window, dict) else window.model_dump()
            w["reset_at"] = get_budget_reset_time(
                budget_duration=w["budget_duration"]
            ).isoformat()
            initialized_windows.append(w)
        updated_kv["budget_limits"] = json.dumps(initialized_windows)

