
def _slice_value(index, context: InferenceContext | None = None):
    """Get the value of the given slice index."""

    if isinstance(index, Const):
        if isinstance(index.value, (int, type(None))):
            return index.value
    elif index is None:
        return None
    else:
        # Try to infer what the index actually is.
        # Since we can't return all the possible values,
        # we'll stop at the first possible value.
        try:
            inferred = next(index.infer(context=context))
        except (InferenceError, StopIteration):
            pass
        else:
            if isinstance(inferred, Const):
                if isinstance(inferred.value, (int, type(None))):
                    return inferred.value

    # Use a sentinel, because None can be a valid
    # value that this function can return,
    # as it is the case for unspecified bounds.
    return _SLICE_SENTINEL

