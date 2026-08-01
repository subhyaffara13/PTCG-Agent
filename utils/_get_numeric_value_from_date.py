
def _get_numeric_value_from_date(date, mask):
    """Converts date (datetime Python object) to a NumericValue object with a Date object value."""
    if date.year < _MIN_YEAR or date.year > _MAX_YEAR:
        raise ValueError(f"Invalid year: {date.year}")

    new_date = Date()
    if mask.year:
        new_date.year = date.year
    if mask.month:
        new_date.month = date.month
    if mask.day:
        new_date.day = date.day
    return NumericValue(date=new_date)

