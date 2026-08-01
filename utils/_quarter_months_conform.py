
def _quarter_months_conform(source: str, target: str) -> bool:
    snum = MONTH_NUMBERS[source]
    tnum = MONTH_NUMBERS[target]
    return snum % 3 == tnum % 3

