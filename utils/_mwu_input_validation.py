
def _mwu_input_validation(x, y, use_continuity, alternative, axis, method):
    ''' Input validation and standardization for mannwhitneyu '''
    xp = array_namespace(x, y)

    if not is_lazy_array(x) and (xp.any(xp.isnan(x)) or xp.any(xp.isnan(y))):
        raise ValueError('`x` and `y` must not contain NaNs.')
    if xp_size(x) == 0 or xp_size(y) == 0:
        raise ValueError('`x` and `y` must be of nonzero size.')
    x, y = xp_promote(x, y, force_floating=True, xp=xp)

    bools = {True, False}
    if use_continuity not in bools:
        raise ValueError(f'`use_continuity` must be one of {bools}.')

    alternatives = {"two-sided", "less", "greater"}
    alternative = alternative.lower()
    if alternative not in alternatives:
        raise ValueError(f'`alternative` must be one of {alternatives}.')

    axis_int = int(axis)
    if axis != axis_int:
        raise ValueError('`axis` must be an integer.')

    if not isinstance(method, stats.PermutationMethod):
        methods = {"asymptotic", "exact", "auto"}
        method = method.lower()
        if method not in methods:
            raise ValueError(f'`method` must be one of {methods}.')

    if is_marray(xp) and method != "asymptotic":
        message = "Only `method='asymptotic'` is compatible with MArrays."
        raise ValueError(message)

    output_z = True if method == 'asymptotic' else False

    return x, y, use_continuity, alternative, axis_int, method, output_z, xp

