
def pattern_bytes_validator(input_value: Any, /) -> re.Pattern[bytes]:
    if isinstance(input_value, re.Pattern):
        if isinstance(input_value.pattern, bytes):
            return input_value
        else:
            raise PydanticCustomError('pattern_bytes_type', 'Input should be a bytes pattern')
    elif isinstance(input_value, bytes):
        return compile_pattern(input_value)
    elif isinstance(input_value, str):
        raise PydanticCustomError('pattern_bytes_type', 'Input should be a bytes pattern')
    else:
        raise PydanticCustomError('pattern_type', 'Input should be a valid pattern')

