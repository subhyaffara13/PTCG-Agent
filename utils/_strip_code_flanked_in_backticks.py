
def _strip_code_flanked_in_backticks(line: str) -> str:
    """Alter line so code flanked in back-ticks is ignored.

    Pyenchant automatically strips back-ticks when parsing tokens,
    so this cannot be done at the individual filter level.
    """

    def replace_code_but_leave_surrounding_characters(match_obj: re.Match[str]) -> str:
        return match_obj.group(1) + match_obj.group(5)

    return CODE_FLANKED_IN_BACKTICK_REGEX.sub(
        replace_code_but_leave_surrounding_characters, line
    )

