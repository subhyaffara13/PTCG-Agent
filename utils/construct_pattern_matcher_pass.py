
def construct_pattern_matcher_pass(pass_name: str):
    """
    Return the specific pattern_matcher_pass given the pass name.
    """
    if pass_name in PRE_GRAD_PATTERNS:
        return PRE_GRAD_PATTERNS[pass_name]
    else:
        return POST_GRAD_PATTERNS[pass_name]

