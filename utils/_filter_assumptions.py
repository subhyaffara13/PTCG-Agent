
def _filter_assumptions(kwargs):
    """Split the given dict into assumptions and non-assumptions.
    Keys are taken as assumptions if they correspond to an
    entry in ``_assume_defined``.
    """
    assumptions, nonassumptions = map(dict, sift(kwargs.items(),
        lambda i: i[0] in _assume_defined,
        binary=True))
    Symbol._sanitize(assumptions)
    return assumptions, nonassumptions

