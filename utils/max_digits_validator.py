
def max_digits_validator(x: Any, max_digits: Any) -> Any:
    try:
        _, num_digits = _extract_decimal_digits_info(x)
        _, normalized_num_digits = _extract_decimal_digits_info(x.normalize())
        if (num_digits > max_digits) and (normalized_num_digits > max_digits):
            raise PydanticKnownError(
                'decimal_max_digits',
                {'max_digits': max_digits},
            )
        return x
    except TypeError:
        raise TypeError(f"Unable to apply constraint 'max_digits' to supplied value {x}")

