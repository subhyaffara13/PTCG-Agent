
def glyphs_to_quadratic(
    glyphs, max_err=None, reverse_direction=False, stats=None, all_quadratic=True
):
    """Convert the curves of a set of compatible of glyphs to quadratic.

    All curves will be converted to quadratic at once, ensuring interpolation
    compatibility. If this is not required, calling glyphs_to_quadratic with one
    glyph at a time may yield slightly more optimized results.

    Empty glyphs (without contours) are ignored and passed through unchanged.

    Return True if glyphs were modified, else return False.

    Raises IncompatibleGlyphsError if glyphs have non-interpolatable outlines.
    """
    if stats is None:
        stats = {}

    if max_err is None:
        # assume 1000 is the default UPEM
        max_err = DEFAULT_MAX_ERR * 1000

    if isinstance(max_err, (list, tuple)):
        max_errors = max_err
    else:
        max_errors = [max_err] * len(glyphs)
    _validate_length(max_errors, len(glyphs), "max_err")
    _validate_positive_tolerances(max_errors, "max_err")

    return _glyphs_to_quadratic(
        glyphs, max_errors, reverse_direction, stats, all_quadratic
    )

