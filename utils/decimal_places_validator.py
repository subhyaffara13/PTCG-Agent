from typing import Any

def decimal_places_validator(x: Any, decimal_places: Any) -> Any:
    try:
        decimal_places_, _ = _extract_decimal_digits_info(x)
        if decimal_places_ > decimal_places:
            normalized_decimal_places, _ = _extract_decimal_digits_info(x.normalize())
            if normalized_decimal_places > decimal_places:
                raise PydanticKnownError(
                    'decimal_max_places',
                    {'decimal_places': decimal_places},
                )
        return x
    except TypeError:
        raise TypeError(f"Unable to apply constraint 'decimal_places' to supplied value {x}")

