
def _has_changed(before: str, after: str, line_separator: str, ignore_whitespace: bool) -> bool:
    if ignore_whitespace:
        return (
            remove_whitespace(before, line_separator=line_separator).strip()
            != remove_whitespace(after, line_separator=line_separator).strip()
        )
    return before.strip() != after.strip()

