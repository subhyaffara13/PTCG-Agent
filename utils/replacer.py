
def replacer(match):
    """
    Finds the correct replacement and applies case based on a specific heuristic.
    """
    original_word = match.group(0)
    replacement = _REPLACEMENT_MAP[original_word.lower()]

    # Rule 1: Preserve ALL CAPS.
    if original_word.isupper():
        return replacement.upper()

    # Rule 2: Handle title-cased words with a more specific heuristic.
    if original_word.istitle():
        # Preserve title case if it's the first word of the string OR
        # if it's a form like "-ing" which can start a new clause.
        return replacement.title()

    # Rule 3: For all other cases (e.g., "Kill" mid-sentence), default to lowercase.
    return replacement.lower()

