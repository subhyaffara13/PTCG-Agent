
def fixed_now_ts() -> Timestamp:
    """
    Fixture emits fixed Timestamp.now()
    """
    return Timestamp(  # pyright: ignore[reportReturnType]
        year=2021, month=1, day=1, hour=12, minute=4, second=13, microsecond=22
    )

