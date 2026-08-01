
def buildAnchor(x, y, point=None, deviceX=None, deviceY=None):
    """Builds an Anchor table.

    This determines the appropriate anchor format based on the passed parameters.

    Args:
        x (int): X coordinate.
        y (int): Y coordinate.
        point (int): Index of glyph contour point, if provided.
        deviceX (``otTables.Device``): X coordinate device table, if provided.
        deviceY (``otTables.Device``): Y coordinate device table, if provided.

    Returns:
        An ``otTables.Anchor`` object.
    """
    self = ot.Anchor()
    self.XCoordinate, self.YCoordinate = x, y
    self.Format = 1
    if point is not None:
        self.AnchorPoint = point
        self.Format = 2
    if deviceX is not None or deviceY is not None:
        assert (
            self.Format == 1
        ), "Either point, or both of deviceX/deviceY, must be None."
        self.XDeviceTable = deviceX
        self.YDeviceTable = deviceY
        self.Format = 3
    return self

