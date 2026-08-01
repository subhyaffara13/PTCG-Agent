
def should_use_regex(regex: bool, to_replace: Any) -> bool:
    """
    Decide whether to treat `to_replace` as a regular expression.
    """
    if is_re(to_replace):
        regex = True

    regex = regex and is_re_compilable(to_replace)

    # Don't use regex if the pattern is empty.
    regex = regex and re.compile(to_replace).pattern != ""
    return regex

