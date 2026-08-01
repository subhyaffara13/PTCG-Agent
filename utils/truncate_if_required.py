
def truncate_if_required(explanation: list[str], item: Item) -> list[str]:
    """Truncate this assertion explanation if the given test item is eligible."""
    should_truncate, max_lines, max_chars = _get_truncation_parameters(item)
    if should_truncate:
        return _truncate_explanation(
            explanation,
            max_lines=max_lines,
            max_chars=max_chars,
        )
    return explanation

