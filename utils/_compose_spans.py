
def _compose_spans(span_matches, spans_name):
    """Takes a list of span matches (expected to be a list of tuples) and a string 
    (the expected span list name) and processes the list so that the values extracted 
    from the span matches can be used to compose a tuple of BucketSpan objects"""
    spans = {}
    for match in span_matches:
        # Extract the key from the match (first element of the tuple).
        key = match[0]
        # Extract the value from the match (second element of the tuple).
        # Split the value string by commas to get individual pairs, 
        # split each pair by ':' to get start and end, and convert them to integers.
        value = [tuple(map(int, pair.split(':'))) for pair in match[1].split(',')]
        # Store the processed value in the spans dictionary with the key.
        spans[key] = value
    if spans_name not in spans:
        return None
    out_spans = []
    # Iterate over each start and end tuple in the list of tuples for the specified spans_name.
    for start, end in spans[spans_name]:
        # Compose a BucketSpan object with the start and end values 
        # and append it to the out_spans list.
        out_spans.append(BucketSpan(start, end))
        # Convert to tuple
    out_spans_tuple = tuple(out_spans)
    return out_spans_tuple

