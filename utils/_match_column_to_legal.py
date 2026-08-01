
def _match_column_to_legal(
    column: str,
    legal_action_strings: Sequence[str],
) -> str | None:
    """Match a column number string to a legal action string."""
    for legal in legal_action_strings:
        if legal.endswith(column):
            return legal
    return None

