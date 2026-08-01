
def _transform(raw_value):
    # TODO assumes a 'matrix' transform.
    # No other transform functions are supported at the moment.
    # https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform
    # start simple: if you aren't exactly matrix(...) then no love
    match = re.match(r"matrix\((.*)\)", raw_value)
    if not match:
        raise NotImplementedError
    matrix = tuple(float(p) for p in re.split(r"\s+|,", match.group(1)))
    if len(matrix) != 6:
        raise ValueError("wrong # of terms in %s" % raw_value)
    return matrix

