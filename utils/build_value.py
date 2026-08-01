
def buildValue(value):
    """Builds a positioning value record.

    Value records are used to specify coordinates and adjustments for
    positioning and attaching glyphs. Many of the positioning functions
    in this library take ``otTables.ValueRecord`` objects as arguments.
    This function builds value records from dictionaries.

    Args:
        value (dict): A dictionary with zero or more of the following keys:
            - ``xPlacement``
            - ``yPlacement``
            - ``xAdvance``
            - ``yAdvance``
            - ``xPlaDevice``
            - ``yPlaDevice``
            - ``xAdvDevice``
            - ``yAdvDevice``

    Returns:
        An ``otTables.ValueRecord`` object.
    """
    self = ValueRecord()
    for k, v in value.items():
        setattr(self, k, v)
    return self

