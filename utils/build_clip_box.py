
def buildClipBox(clipBox: _ClipBoxInput) -> ot.ClipBox:
    if isinstance(clipBox, ot.ClipBox):
        return clipBox
    n = len(clipBox)
    clip = ot.ClipBox()
    if n not in (4, 5):
        raise ValueError(f"Invalid ClipBox: expected 4 or 5 values, found {n}")
    clip.xMin, clip.yMin, clip.xMax, clip.yMax = intRect(clipBox[:4])
    clip.Format = int(n == 5) + 1
    if n == 5:
        clip.VarIndexBase = int(clipBox[4])
    return clip

