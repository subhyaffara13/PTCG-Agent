from typing import Any, Callable, Optional

def _writeGlyphToBytes(
    glyphName: str,
    glyphObject: Optional[Any] = None,
    drawPointsFunc: Optional[Callable[[Any], None]] = None,
    writer: Optional[Any] = None,
    formatVersion: Optional[FormatVersion] = None,
    validate: bool = True,
) -> bytes:
    """Return .glif data for a glyph as a UTF-8 encoded bytes string."""
    try:
        formatVersion = normalizeFormatVersion(formatVersion, GLIFFormatVersion)
    except ValueError:
        from fontTools.ufoLib.errors import UnsupportedGLIFFormat

        raise UnsupportedGLIFFormat(
            "Unsupported GLIF format version: {formatVersion!r}"
        )
    # start
    if validate and not isinstance(glyphName, str):
        raise GlifLibError("The glyph name is not properly formatted.")
    if validate and len(glyphName) == 0:
        raise GlifLibError("The glyph name is empty.")
    glyphAttrs = OrderedDict(
        [("name", glyphName), ("format", repr(formatVersion.major))]
    )
    if formatVersion.minor != 0:
        glyphAttrs["formatMinor"] = repr(formatVersion.minor)
    root = etree.Element("glyph", glyphAttrs)
    identifiers: set[str] = set()
    # advance
    _writeAdvance(glyphObject, root, validate)
    # unicodes
    if getattr(glyphObject, "unicodes", None):
        _writeUnicodes(glyphObject, root, validate)
    # note
    if getattr(glyphObject, "note", None):
        _writeNote(glyphObject, root, validate)
    # image
    if formatVersion.major >= 2 and getattr(glyphObject, "image", None):
        _writeImage(glyphObject, root, validate)
    # guidelines
    if formatVersion.major >= 2 and getattr(glyphObject, "guidelines", None):
        _writeGuidelines(glyphObject, root, identifiers, validate)
    # anchors
    anchors = getattr(glyphObject, "anchors", None)
    if formatVersion.major >= 2 and anchors:
        _writeAnchors(glyphObject, root, identifiers, validate)
    # outline
    if drawPointsFunc is not None:
        outline = etree.SubElement(root, "outline")
        pen = GLIFPointPen(outline, identifiers=identifiers, validate=validate)
        drawPointsFunc(pen)
        if formatVersion.major == 1 and anchors:
            _writeAnchorsFormat1(pen, anchors, validate)
        # prevent lxml from writing self-closing tags
        if not len(outline):
            outline.text = "\n  "
    # lib
    if getattr(glyphObject, "lib", None):
        _writeLib(glyphObject, root, validate)
    # return the text
    data = etree.tostring(
        root, encoding="UTF-8", xml_declaration=True, pretty_print=True
    )
    return data

