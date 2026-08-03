from typing import Optional

def _validate_tag_list_date_range(
    start_date: Optional[str], end_date: Optional[str]
) -> None:
    """Require both dates together, and enforce YYYY-MM-DD format with start <= end."""
    if (start_date is None) != (end_date is None):
        raise HTTPException(
            status_code=400,
            detail="start_date and end_date must be provided together",
        )
    if start_date is None:
        return
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")  # type: ignore[arg-type]
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid date format, expected YYYY-MM-DD: {e}",
        )
    if start > end:
        raise HTTPException(
            status_code=400,
            detail="start_date must be on or before end_date",
        )

