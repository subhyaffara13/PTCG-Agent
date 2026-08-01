
def basic_count(text: str) -> int:
    """Split the string and ignore punctuation only elements."""
    return sum([el.strip(string.punctuation).isalpha() for el in text.split()])

