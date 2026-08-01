
def planSlantAxis(
    glyphSetFunc,
    axisLimits,
    slants=None,
    samples=None,
    glyphs=None,
    designLimits=None,
    pins=None,
    sanitize=False,
):
    """Plan a slant (`slnt`) axis.

    slants: A list slant angles to plan for. If None, the default
    values are used.

    This function simply calls planAxis with values=slants, and the appropriate
    arguments. See documenation for planAxis for more information.
    """

    if slants is None:
        slants = SLANTS

    return planAxis(
        measureSlant,
        normalizeDegrees,
        interpolateLinear,
        glyphSetFunc,
        "slnt",
        axisLimits,
        values=slants,
        samples=samples,
        glyphs=glyphs,
        designLimits=designLimits,
        pins=pins,
        sanitizeFunc=sanitizeSlant if sanitize else None,
    )

