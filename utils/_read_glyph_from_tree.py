from typing import Any, Optional, Set

def _readGlyphFromTree(
    tree: ElementType,
    glyphObject: Optional[Any] = None,
    pointPen: Optional[AbstractPointPen] = None,
    formatVersions: Set[GLIFFormatVersion] = GLIFFormatVersion.supported_versions(),
    validate: bool = True,
) -> None:
    # check the format version
    formatVersionMajor = tree.get("format")
    if formatVersionMajor is None:
        if validate:
            raise GlifLibError("Unspecified format version in GLIF.")
        formatVersionMajor = 0
    formatVersionMinor = tree.get("formatMinor", 0)
    try:
        formatVersion = GLIFFormatVersion(
            (int(formatVersionMajor), int(formatVersionMinor))
        )
    except ValueError as e:
        msg = "Unsupported GLIF format: %s.%s" % (
            formatVersionMajor,
            formatVersionMinor,
        )
        if validate:
            from fontTools.ufoLib.errors import UnsupportedGLIFFormat

            raise UnsupportedGLIFFormat(msg) from e
        # warn but continue using the latest supported format
        formatVersion = GLIFFormatVersion.default()
        logger.warning(
            "%s. Assuming the latest supported version (%s). "
            "Some data may be skipped or parsed incorrectly.",
            msg,
            formatVersion,
        )

    if validate and formatVersion not in formatVersions:
        raise GlifLibError(f"Forbidden GLIF format version: {formatVersion!s}")

    try:
        readGlyphFromTree = _READ_GLYPH_FROM_TREE_FUNCS[formatVersion]
    except KeyError:
        raise NotImplementedError(formatVersion)

    readGlyphFromTree(
        tree=tree,
        glyphObject=glyphObject,
        pointPen=pointPen,
        validate=validate,
        formatMinor=formatVersion.minor,
    )

