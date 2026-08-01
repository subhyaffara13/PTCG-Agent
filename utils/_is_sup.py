
def _is_sup(f1: str, f2: str) -> bool:
    return (f1.startswith("W") and is_superperiod("D", f2)) or (
        f2.startswith("W") and is_superperiod(f1, "D")
    )

