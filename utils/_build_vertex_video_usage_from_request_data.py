from typing import Any, Dict, Optional

def _build_vertex_video_usage_from_request_data(
    request_data: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Build usage metadata (duration, resolution) for video cost calculation."""
    usage_data: Dict[str, Any] = {}
    if not request_data:
        return usage_data

    parameters = request_data.get("parameters", {})
    duration = (
        parameters.get("durationSeconds") or DEFAULT_GOOGLE_VIDEO_DURATION_SECONDS
    )
    if duration is not None:
        try:
            usage_data["duration_seconds"] = float(duration)
        except (ValueError, TypeError):
            pass
    res = parameters.get("resolution")
    if res is not None and str(res).strip() != "":
        usage_data["video_resolution"] = str(res).strip().lower()
    return usage_data

