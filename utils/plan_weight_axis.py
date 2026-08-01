
def planWeightAxis(
    glyphSetFunc,
    axisLimits,
    weights=None,
    samples=None,
    glyphs=None,
    designLimits=None,
    pins=None,
    sanitize=False,
):
    """Plan a weight (`wght`) axis.

    weights: A list of weight values to plan for. If None, the default
    values are used.

    This function simply calls planAxis with values=weights, and the appropriate
    arguments. See documenation for planAxis for more information.
    """

    if weights is None:
        weights = WEIGHTS

    return planAxis(
        measureWeight,
        normalizeLinear,
        interpolateLog,
        glyphSetFunc,
        "wght",
        axisLimits,
        values=weights,
        samples=samples,
        glyphs=glyphs,
        designLimits=designLimits,
        pins=pins,
        sanitizeFunc=sanitizeWeight if sanitize else None,
    )

