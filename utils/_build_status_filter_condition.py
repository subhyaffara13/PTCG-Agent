
def _build_status_filter_condition(status_filter: Optional[str]) -> Dict[str, Any]:
    """
    Helper function to build the status filter condition for database queries.

    Args:
        status_filter (Optional[str]): The status to filter by. Can be "success" or "failure".

    Returns:
        Dict[str, Any]: A dictionary containing the status filter condition.
    """
    if status_filter is None:
        return {}

    if status_filter == "success":
        return {"OR": [{"status": {"equals": "success"}}, {"status": None}]}
    else:
        return {"status": {"equals": status_filter}}

