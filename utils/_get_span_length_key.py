
def _get_span_length_key(span):
    """Sorts span by decreasing length first and increasing first index second."""
    return span[1] - span[0], -span[0]

