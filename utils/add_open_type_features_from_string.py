
def addOpenTypeFeaturesFromString(
    font, features, filename=None, tables=None, debug=False
):
    """Add features from a string to a font. Note that this replaces any
    features currently present.

    Args:
        font (feaLib.ttLib.TTFont): The font object.
        features: A string containing feature code.
        filename: The directory containing ``filename`` is used as the root of
            relative ``include()`` paths; if ``None`` is provided, the current
            directory is assumed.
        tables: If passed, restrict the set of affected tables to those in the
            list.
        debug: Whether to add source debugging information to the font in the
            ``Debg`` table

    """

    featurefile = StringIO(tostr(features))
    if filename:
        featurefile.name = filename
    addOpenTypeFeatures(font, featurefile, tables=tables, debug=debug)

