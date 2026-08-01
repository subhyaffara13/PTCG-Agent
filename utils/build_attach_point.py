
def buildAttachPoint(points):
    # [4, 23, 41] --> otTables.AttachPoint
    # Only used by above.
    if not points:
        return None
    self = ot.AttachPoint()
    self.PointIndex = sorted(set(points))
    self.PointCount = len(self.PointIndex)
    return self

