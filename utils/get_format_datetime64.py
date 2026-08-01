
def get_format_datetime64(
    is_dates_only: bool, nat_rep: str = "NaT", date_format: str | None = None
) -> Callable:
    """Return a formatter callable taking a datetime64 as input and providing
    a string as output"""

    if is_dates_only:
        return lambda x: _format_datetime64_dateonly(
            x, nat_rep=nat_rep, date_format=date_format
        )
    else:
        return lambda x: _format_datetime64(x, nat_rep=nat_rep)

