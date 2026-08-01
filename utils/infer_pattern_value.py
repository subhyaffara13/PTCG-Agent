
def infer_pattern_value(pattern: Pattern) -> int:
    if isinstance(pattern, AsPattern) and pattern.pattern is None:
        return ALWAYS_TRUE
    elif isinstance(pattern, OrPattern) and any(
        infer_pattern_value(p) == ALWAYS_TRUE for p in pattern.patterns
    ):
        return ALWAYS_TRUE
    else:
        return TRUTH_VALUE_UNKNOWN

