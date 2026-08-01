
def to_int_us(v: float | None) -> int | None:
    return None if v is None else int(v * 1_000_000)

