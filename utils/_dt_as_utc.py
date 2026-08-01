
def _dt_as_utc(dt: None) -> None: ...


def _dt_as_utc(dt: datetime) -> datetime: ...


def _dt_as_utc(dt: datetime | None) -> datetime | None:
    if dt is None:
        return dt

    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    elif dt.tzinfo != timezone.utc:
        return dt.astimezone(timezone.utc)

    return dt

