
def updateNameTable(varfont, axisLimits):
    """Update instatiated variable font's name table using STAT AxisValues.

    Raises ValueError if the STAT table is missing or an Axis Value table is
    missing for requested axis locations.

    First, collect all STAT AxisValues that match the new default axis locations
    (excluding "elided" ones); concatenate the strings in design axis order,
    while giving priority to "synthetic" values (Format 4), to form the
    typographic subfamily name associated with the new default instance.
    Finally, update all related records in the name table, making sure that
    legacy family/sub-family names conform to the the R/I/B/BI (Regular, Italic,
    Bold, Bold Italic) naming model.

    Example: Updating a partial variable font:
    | >>> ttFont = TTFont("OpenSans[wdth,wght].ttf")
    | >>> updateNameTable(ttFont, {"wght": (400, 900), "wdth": 75})

    The name table records will be updated in the following manner:
    NameID 1 familyName: "Open Sans" --> "Open Sans Condensed"
    NameID 2 subFamilyName: "Regular" --> "Regular"
    NameID 3 Unique font identifier: "3.000;GOOG;OpenSans-Regular" --> \
        "3.000;GOOG;OpenSans-Condensed"
    NameID 4 Full font name: "Open Sans Regular" --> "Open Sans Condensed"
    NameID 6 PostScript name: "OpenSans-Regular" --> "OpenSans-Condensed"
    NameID 16 Typographic Family name: None --> "Open Sans"
    NameID 17 Typographic Subfamily name: None --> "Condensed"

    References:
    https://docs.microsoft.com/en-us/typography/opentype/spec/stat
    https://docs.microsoft.com/en-us/typography/opentype/spec/name#name-ids
    """
    from . import AxisLimits, axisValuesFromAxisLimits

    if "STAT" not in varfont:
        raise ValueError("Cannot update name table since there is no STAT table.")
    stat = varfont["STAT"].table
    if not stat.AxisValueArray:
        raise ValueError("Cannot update name table since there are no STAT Axis Values")
    fvar = varfont["fvar"]

    # The updated name table will reflect the new 'zero origin' of the font.
    # If we're instantiating a partial font, we will populate the unpinned
    # axes with their default axis values from fvar.
    axisLimits = AxisLimits(axisLimits).limitAxesAndPopulateDefaults(varfont)
    partialDefaults = axisLimits.defaultLocation()
    fvarDefaults = {a.axisTag: a.defaultValue for a in fvar.axes}
    defaultAxisCoords = AxisLimits({**fvarDefaults, **partialDefaults})
    assert all(v.minimum == v.maximum for v in defaultAxisCoords.values())

    axisValueTables = axisValuesFromAxisLimits(stat, defaultAxisCoords)
    checkAxisValuesExist(stat, axisValueTables, defaultAxisCoords.pinnedLocation())

    # ignore "elidable" axis values, should be omitted in application font menus.
    axisValueTables = [
        v for v in axisValueTables if not v.Flags & ELIDABLE_AXIS_VALUE_NAME
    ]
    axisValueTables = _sortAxisValues(axisValueTables)
    _updateNameRecords(varfont, axisValueTables)

