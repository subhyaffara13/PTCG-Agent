
def _usage_video_resolution_from_parameters(
    parameters: Dict[str, Any],
) -> Optional[str]:
    """Normalize Veo ``parameters.resolution`` for usage and cost tracking."""
    res = parameters.get("resolution")
    if res is None or res == "":
        return None
    return str(res).strip().lower()

