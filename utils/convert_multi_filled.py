
def convert_multi_filled(
    multi_filled: list[cpy.FillReturn],
    fill_type_from: FillType | str,
    fill_type_to:  FillType | str,
) -> list[cpy.FillReturn]:
    """Convert multiple sets of filled contours from one :class:`~.FillType` to another.

    Args:
        multi_filled (nested sequence of arrays): Filled contour polygons to convert, such as those
            returned by :meth:`.ContourGenerator.multi_filled`.
        fill_type_from (FillType or str): :class:`~.FillType` to convert from as enum or
            string equivalent.
        fill_type_to (FillType or str): :class:`~.FillType` to convert to as enum or string
            equivalent.

    Return:
        Converted sets filled contour polygons.

    When converting non-chunked fill types (``FillType.OuterCode`` or ``FillType.OuterOffset``) to
    chunked ones, all polygons are placed in the first chunk. When converting in the other
    direction, all chunk information is discarded. Converting a fill type that is not aware of the
    relationship between outer boundaries and contained holes (``FillType.ChunkCombinedCode`` or
    ``FillType.ChunkCombinedOffset``) to one that is will raise a ``ValueError``.

    .. versionadded:: 1.3.0
    """
    fill_type_from = as_fill_type(fill_type_from)
    fill_type_to = as_fill_type(fill_type_to)

    return [convert_filled(filled, fill_type_from, fill_type_to) for filled in multi_filled]

