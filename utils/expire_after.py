
def expire_after(delta: timedelta, date: datetime | None = None) -> datetime:
    date = date or datetime.now(timezone.utc)
    return date + delta


def expire_after(delta: timedelta, date: datetime | None = None) -> datetime:
    date = date or datetime.now(timezone.utc)
    return date + delta

