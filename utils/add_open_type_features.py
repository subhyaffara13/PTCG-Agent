
def addOpenTypeFeatures(font, featurefile, tables=None, debug=False):
    """Add features from a file to a font. Note that this replaces any features
    currently present.

    Args:
        font (feaLib.ttLib.TTFont): The font object.
        featurefile: Either a path or file object (in which case we
            parse it into an AST), or a pre-parsed AST instance.
        tables: If passed, restrict the set of affected tables to those in the
            list.
        debug: Whether to add source debugging information to the font in the
            ``Debg`` table

    """
    builder = Builder(font, featurefile)
    builder.build(tables=tables, debug=debug)

