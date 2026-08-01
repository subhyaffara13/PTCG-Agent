
def register_freezing_graph_pattern(pattern, extra_check=_return_true, pass_number=0):
    while pass_number > len(pass_patterns) - 1:
        pass_patterns.append(PatternMatcherPass())
    return register_graph_pattern(
        pattern,
        extra_check=extra_check,
        # pyrefly: ignore [bad-argument-type]
        pass_dict=pass_patterns[pass_number],
    )

