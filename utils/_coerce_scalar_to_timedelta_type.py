
def _coerce_scalar_to_timedelta_type(
    r, unit: UnitChoices | None = "ns", errors: DateTimeErrorChoices = "raise"
) -> Timedelta | NaTType:
    """Convert string 'r' to a timedelta object."""
    result: Timedelta | NaTType

    try:
        result = Timedelta(r, unit)
    except ValueError:
        if errors == "raise":
            raise
        # coerce
        result = NaT

    return result

