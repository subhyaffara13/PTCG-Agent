from typing import Optional

def _get_request_duration_ms(start_time: datetime, end_time: datetime) -> Optional[int]:
    """Compute request duration in milliseconds from start and end times."""
    try:
        return int((end_time - start_time).total_seconds() * 1000)
    except Exception:
        return None

