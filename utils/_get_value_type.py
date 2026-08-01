
def _get_value_type(numeric_value):
    if numeric_value.float_value is not None:
        return NUMBER_TYPE
    elif numeric_value.date is not None:
        return DATE_TYPE
    raise ValueError(f"Unknown type: {numeric_value}")

