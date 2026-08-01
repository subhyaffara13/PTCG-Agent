
def _f_oneway_is_too_small(samples, kwargs=None, axis=-1):
    message = f"At least two samples are required; got {len(samples)}."
    if len(samples) < 2:
        raise TypeError(message)

    # Check this after forming alldata, so shape errors are detected
    # and reported before checking for 0 length inputs.
    if any(sample.shape[axis] == 0 for sample in samples):
        return True

    # Must have at least one group with length greater than 1.
    if all(sample.shape[axis] == 1 for sample in samples):
        msg = ('all input arrays have length 1.  f_oneway requires that at '
               'least one input has length greater than 1.')
        warnings.warn(SmallSampleWarning(msg), stacklevel=2)
        return True

    return False

