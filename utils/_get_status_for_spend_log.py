
def _get_status_for_spend_log(
    metadata: dict,
) -> Literal["success", "failure"]:
    """
    Get the status for the spend log.

    It's only a failure if metadata.get("status") is "failure"
    """
    _status: Optional[str] = metadata.get("status", None)
    if _status == "failure":
        return "failure"
    return "success"

