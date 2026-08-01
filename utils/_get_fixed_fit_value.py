
def _get_fixed_fit_value(kwds, names):
    """
    Given names such as ``['f0', 'fa', 'fix_a']``, check that there is
    at most one non-None value in `kwds` associated with those names.
    Return that value, or None if none of the names occur in `kwds`.
    As a side effect, all occurrences of those names in `kwds` are
    removed.
    """
    vals = [(name, kwds.pop(name)) for name in names if name in kwds]
    if len(vals) > 1:
        repeated = [name for name, val in vals]
        raise ValueError("fit method got multiple keyword arguments to "
                         "specify the same fixed parameter: " +
                         ', '.join(repeated))
    return vals[0][1] if vals else None

