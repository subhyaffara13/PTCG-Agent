
def qconfig_equals(q1: QConfigAny, q2: QConfigAny):
    """
    Returns `True` if `q1` equals `q2`, and `False` otherwise.
    """
    if q1 is None or q2 is None:
        return q1 == q2
    else:
        if q1 is None or q2 is None:
            raise AssertionError(
                "Both q1 and q2 must be non-None for qconfig comparison"
            )
        try:
            # Qconfig weight and activation can be either a partial wrapper,
            # or an observer class. Special handling is required (above) for
            # comparing partial wrappers.
            activation_same = _obs_or_fq_ctr_equals(q1.activation, q2.activation)
            weight_same = _obs_or_fq_ctr_equals(q1.weight, q2.weight)
            return activation_same and weight_same
        except AttributeError:
            return q1 == q2

