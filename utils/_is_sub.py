
def _is_sub(f1: str, f2: str) -> bool:
    return (f1.startswith("W") and is_subperiod("D", f2)) or (
        f2.startswith("W") and is_subperiod(f1, "D")
    )

