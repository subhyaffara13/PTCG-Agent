
def _summary_stats(xs: list[int]) -> tuple[float, float]:
    if not xs:
        return float("nan"), float("nan")
    return statistics.mean(xs), statistics.pstdev(xs)

