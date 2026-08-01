
def pattern_str_validator(input_value: Any, /) -> re.Pattern[str]:
    if isinstance(input_value, re.Pattern):
        if isinstance(input_value.pattern, str):
            return input_value
        else:
            raise PydanticCustomError('pattern_str_type', 'Input should be a string pattern')
    elif isinstance(input_value, str):
        return compile_pattern(input_value)
    elif isinstance(input_value, bytes):
        raise PydanticCustomError('pattern_str_type', 'Input should be a string pattern')
    else:
        raise PydanticCustomError('pattern_type', 'Input should be a valid pattern')

