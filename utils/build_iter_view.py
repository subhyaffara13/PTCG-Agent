
def build_iter_view(matches: Matches[CT]) -> Iterable[CT]:
    """Build an iterable view from the value returned by `find_matches()`."""
    if callable(matches):
        return _FactoryIterableView(matches)
    if not isinstance(matches, Sequence):
        matches = list(matches)
    return _SequenceIterableView(matches)

