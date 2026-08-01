
def period_start(day: date, interval: PartitionInterval) -> date:
    """First day of the partition period that `day` falls into (UTC)."""
    if interval == "day":
        return day
    if interval == "week":
        return day - timedelta(days=day.weekday())
    if interval == "month":
        return day.replace(day=1)
    raise ValueError(f"Unsupported partition interval: {interval}")

