
def mi_compute(halstead_volume, complexity, sloc, comments):
    '''Compute the Maintainability Index (MI) given the Halstead Volume, the
    Cyclomatic Complexity, the SLOC number and the number of comment lines.
    Usually it is not used directly but instead :func:`~radon.metrics.mi_visit`
    is preferred.
    '''
    if any(metric <= 0 for metric in (halstead_volume, sloc)):
        return 100.0
    sloc_scale = math.log(sloc)
    volume_scale = math.log(halstead_volume)
    comments_scale = math.sqrt(2.46 * math.radians(comments))
    # Non-normalized MI
    nn_mi = (
        171
        - 5.2 * volume_scale
        - 0.23 * complexity
        - 16.2 * sloc_scale
        + 50 * math.sin(comments_scale)
    )
    return min(max(0.0, nn_mi * 100 / 171.0), 100.0)

