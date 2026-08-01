
def black_invariant(text, chars=None):
    """Remove characters that may be changed when reformatting the text with black"""
    if chars is None:
        chars = [" ", "\t", "\n", ",", "'", '"', "(", ")", "\\"]

    for char in chars:
        text = text.replace(char, "")
    return text

