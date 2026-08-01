
def format_speedup(
    speedup: float,
    pvalue: float,
    is_correct: bool = True,
    pvalue_threshold: float = 0.1,
) -> str:
    if not is_correct:
        return "ERROR"
    if pvalue > pvalue_threshold:
        return f"{speedup:.3f}x SAME"
    return f"{speedup:.3f}x p={pvalue:.2f}"

