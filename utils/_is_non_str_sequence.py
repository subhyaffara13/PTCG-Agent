
def _isNonStrSequence(value):
    return isinstance(value, collections.abc.Sequence) and not isinstance(value, str)

