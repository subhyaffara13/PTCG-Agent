
def _is_list_of_candidate_labels(text) -> bool:
    """Check that text is list/tuple of strings and each string is a candidate label and not merged candidate labels text.
    Merged candidate labels text is a string with candidate labels separated by a dot.
    """
    if isinstance(text, (list, tuple)):
        return all(isinstance(t, str) and "." not in t for t in text)
    return False

