
def _is_quote_delimiter_chosen_freely(string_token: str) -> bool:
    """Was there a non-awkward option for the quote delimiter?

    Args:
        string_token: The quoted string whose delimiters are to be checked.

    Returns:
        Whether there was a choice in this token's quote character that would
        not have involved backslash-escaping an interior quote character.  Long
        strings are excepted from this analysis under the assumption that their
        quote characters are set by policy.
    """
    quote_delimiter = _get_quote_delimiter(string_token)
    unchosen_delimiter = '"' if quote_delimiter == "'" else "'"
    return bool(
        quote_delimiter
        and not _is_long_string(string_token)
        and unchosen_delimiter not in str_eval(string_token)
    )

