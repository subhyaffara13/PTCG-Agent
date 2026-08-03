from typing import List, Tuple

def upcoming_partitions(
    today: date, interval: PartitionInterval, ahead: int
) -> List[Tuple[str, date, date]]:
    """
    Specs (name, lower_inclusive, upper_exclusive) for the current period plus
    the next `ahead` periods, so writes always have a partition to land in.
    """
    specs: List[Tuple[str, date, date]] = []
    start = period_start(today, interval)
    for _ in range(ahead + 1):
        upper = next_period_start(start, interval)
        specs.append((partition_name(start), start, upper))
        start = upper
    return specs

