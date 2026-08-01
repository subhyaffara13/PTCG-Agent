
def next_period_start(start: date, interval: PartitionInterval) -> date:
    if interval == "day":
        return start + timedelta(days=1)
    if interval == "week":
        return start + timedelta(days=7)
    if interval == "month":
        if start.month == 12:
            return start.replace(year=start.year + 1, month=1)
        return start.replace(month=start.month + 1)
    raise ValueError(f"Unsupported partition interval: {interval}")

