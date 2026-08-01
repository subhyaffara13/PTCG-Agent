
def _encode_complex_values(values: dict[complex, int]) -> list[str]:
    """Encode float values into a C array values.

    The result contains the number of values followed by pairs of doubles
    representing complex numbers.
    """
    value_by_index = {index: value for value, index in values.items()}
    result = []
    num = len(values)
    result.append(str(num))
    for i in range(num):
        value = value_by_index[i]
        result.append(float_to_c(value.real))
        result.append(float_to_c(value.imag))
    return result

