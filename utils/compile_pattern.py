
def compile_pattern(pattern: PatternType) -> re.Pattern[PatternType]:
    try:
        return re.compile(pattern)
    except re.error:
        raise PydanticCustomError('pattern_regex', 'Input should be a valid regular expression')

