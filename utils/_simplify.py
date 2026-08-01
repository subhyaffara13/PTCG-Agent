
def _simplify(expr, doit):
    if doit:
        from sympy.simplify import simplify
        from sympy.simplify.powsimp import powdenest
        return simplify(powdenest(piecewise_fold(expr), polar=True))
    return expr


def _simplify(expr):
    """ Wrapper to avoid circular imports. """
    from sympy.simplify.simplify import simplify
    return simplify(expr)


def _simplify(
    path: pathops.Path,
    debugGlyphName: str,
    *,
    round: Callable[[float], float] = otRound,
) -> pathops.Path:
    # skia-pathops has a bug where it sometimes fails to simplify paths when there
    # are float coordinates and control points are very close to one another.
    # Rounding coordinates to integers works around the bug.
    # Since we are going to round glyf coordinates later on anyway, here it is
    # ok(-ish) to also round before simplify. Better than failing the whole process
    # for the entire font.
    # https://bugs.chromium.org/p/skia/issues/detail?id=11958
    # https://github.com/google/fonts/issues/3365
    # TODO(anthrotype): remove once this Skia bug is fixed
    try:
        return pathops.simplify(path, clockwise=path.clockwise)
    except pathops.PathOpsError:
        pass

    path = _round_path(path, round=round)
    try:
        path = pathops.simplify(path, clockwise=path.clockwise)
        log.debug(
            "skia-pathops failed to simplify '%s' with float coordinates, "
            "but succeded using rounded integer coordinates",
            debugGlyphName,
        )
        return path
    except pathops.PathOpsError as e:
        if log.isEnabledFor(logging.DEBUG):
            path.dump()
        raise RemoveOverlapsError(
            f"Failed to remove overlaps from glyph {debugGlyphName!r}"
        ) from e

    raise AssertionError("Unreachable")

