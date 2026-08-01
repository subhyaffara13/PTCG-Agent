
def dechunk_multi_filled(
    multi_filled: list[cpy.FillReturn],
    fill_type: FillType | str,
) -> list[cpy.FillReturn]:
    """Return multiple sets of filled contours with chunked data moved into the first chunks.

    Filled contours that are not chunked (``FillType.OuterCode`` and ``FillType.OuterOffset``) and
    those that are but only contain a single chunk are returned unmodified. Individual polygons are
    unchanged, they are not geometrically combined.

    Args:
        multi_filled (nested sequence of arrays): Filled contour data, such as returned by
            :meth:`.ContourGenerator.multi_filled`.
        fill_type (FillType or str): Type of :meth:`~.ContourGenerator.filled` as enum or string
            equivalent.

    Return:
        Multiple sets of filled contours in a single chunk.

    .. versionadded:: 1.3.0
    """
    fill_type = as_fill_type(fill_type)

    if fill_type in (FillType.OuterCode, FillType.OuterOffset):
        # No-op if fill_type is not chunked.
        return multi_filled

    return [dechunk_filled(filled, fill_type) for filled in multi_filled]

