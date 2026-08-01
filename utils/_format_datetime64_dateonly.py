
def _format_datetime64_dateonly(
    x: NaTType | Timestamp,
    nat_rep: str = "NaT",
    date_format: str | None = None,
) -> str:
    if isinstance(x, NaTType):
        return nat_rep

    if date_format:
        return x.strftime(date_format)
    else:
        # Timestamp._date_repr relies on string formatting (faster than strftime)
        return x._date_repr

