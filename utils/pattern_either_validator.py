
def pattern_either_validator(input_value: Any, /) -> re.Pattern[Any]:
    if isinstance(input_value, re.Pattern):
        return input_value
    elif isinstance(input_value, (str, bytes)):
        # todo strict mode
        return compile_pattern(input_value)  # type: ignore
    else:
        raise PydanticCustomError('pattern_type', 'Input should be a valid pattern')

