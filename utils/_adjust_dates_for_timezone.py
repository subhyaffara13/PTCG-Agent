from typing import Optional, Tuple

def _adjust_dates_for_timezone(
    start_date: str,
    end_date: str,
    timezone_offset_minutes: Optional[int],
) -> Tuple[str, str]:
    """
    Pass-through for the local date range; the timezone offset is intentionally ignored here.

    The aggregation table (e.g. LiteLLM_DailyUserSpend) stores spend in whole-UTC-day
    buckets keyed on date as YYYY-MM-DD. Any conversion from a local date range to a
    UTC date range using only date arithmetic must round to whole UTC days, allowing up
    to 24h of slop at each boundary. The previous implementation expanded the SQL range
    by an extra full UTC day on whichever side the offset pointed, which pulled in 24h
    of unrelated bucket data per boundary and produced approximately 100% over-counting
    on single-day queries (e.g. IST May 29 returning UTC May 28 + UTC May 29 in full).
    Sums of single-day queries then exceeded the equivalent multi-day aggregate, which
    is mathematically impossible.

    Treating the local date as the UTC date trades a small one-time boundary slop for
    correct, monotonic, additive results across single-day and multi-day queries. A
    later fix can introduce hour-level buckets or pro-rata weighting on adjacent UTC
    days; both require data the current schema does not store.
    """
    return start_date, end_date

