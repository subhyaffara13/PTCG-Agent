from typing import List, Optional, Tuple

def select_partitions_to_drop(
    partitions: List[Tuple[str, Optional[datetime]]], cutoff: datetime
) -> List[str]:
    """
    Names of partitions whose entire range is older than `cutoff` (upper bound
    <= cutoff). `cutoff` and the bounds are UTC-naive. Partitions without a
    parseable upper bound (e.g. DEFAULT) are kept.
    """
    return [name for name, upper in partitions if upper is not None and upper <= cutoff]

