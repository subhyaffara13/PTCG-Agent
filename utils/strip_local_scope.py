
def strip_local_scope(s: str) -> str:
    """
    Replace occurrences of L[...] with just the inner content.
    Handles both single and double quotes.

    This is to generate user friendly recompilation messages.
    """
    import re

    pattern = r"L\[\s*['\"](.*?)['\"]\s*\]"
    return re.sub(pattern, r"\1", s)

