
def _get_numeric_values(text):
    """Parses text and returns numeric values."""
    numeric_spans = parse_text(text)
    return itertools.chain(*(span.values for span in numeric_spans))

