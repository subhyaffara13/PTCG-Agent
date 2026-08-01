
def _get_first_match(expr, pattern):
    from matchpy import ManyToOneMatcher, Pattern

    matcher = ManyToOneMatcher()
    matcher.add(Pattern(pattern))
    return next(iter(matcher.match(expr)))

