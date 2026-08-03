from typing import Any, Optional

def get_budget_window_start(window: Any) -> Optional[datetime]:
    window_dict = _coerce_window(window)
    budget_duration = window_dict.get("budget_duration")
    if budget_duration is None:
        return None
    try:
        duration_seconds = duration_in_seconds(str(budget_duration))
    except Exception:
        return None

    reset_at = _coerce_datetime(window_dict.get("reset_at"))
    if reset_at is None:
        return datetime.now(timezone.utc) - timedelta(seconds=duration_seconds)
    if reset_at.tzinfo is None:
        reset_at = reset_at.replace(tzinfo=timezone.utc)
    return reset_at - timedelta(seconds=duration_seconds)

