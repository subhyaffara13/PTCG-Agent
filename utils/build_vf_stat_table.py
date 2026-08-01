
def buildVFStatTable(ttFont: TTFont, doc: DesignSpaceDocument, vfName: str) -> None:
    """Build the STAT table for the variable font identified by its name in
    the given document.

    Knowing which variable we're building STAT data for is needed to subset
    the STAT locations to only include what the variable font actually ships.

    .. versionadded:: 5.0

    .. seealso::
        - :func:`getStatAxes()`
        - :func:`getStatLocations()`
        - :func:`fontTools.otlLib.builder.buildStatTable()`
    """
    for vf in doc.getVariableFonts():
        if vf.name == vfName:
            break
    else:
        raise DesignSpaceDocumentError(
            f"Cannot find the variable font by name {vfName}"
        )

    region = getVFUserRegion(doc, vf)

    # if there are not currently any mac names don't add them here, that's inconsistent
    # https://github.com/fonttools/fonttools/issues/683
    macNames = any(
        nr.platformID == 1 for nr in getattr(ttFont.get("name"), "names", ())
    )

    return fontTools.otlLib.builder.buildStatTable(
        ttFont,
        getStatAxes(doc, region),
        getStatLocations(doc, region),
        doc.elidedFallbackName if doc.elidedFallbackName is not None else 2,
        macNames=macNames,
    )

