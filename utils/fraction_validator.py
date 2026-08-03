from typing import Any

def fraction_validator(input_value: Any, /) -> Fraction:
    if isinstance(input_value, Fraction):
        return input_value

    try:
        return Fraction(input_value)
    except ValueError:
        raise PydanticCustomError('fraction_parsing', 'Input is not a valid fraction')

