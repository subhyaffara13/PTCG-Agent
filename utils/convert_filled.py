
def convert_filled(
    filled: cpy.FillReturn,
    fill_type_from: FillType | str,
    fill_type_to:  FillType | str,
) -> cpy.FillReturn:
    """Convert filled contours from one :class:`~.FillType` to another.

    Args:
        filled (sequence of arrays): Filled contour polygons to convert, such as those returned by
            :meth:`.ContourGenerator.filled`.
        fill_type_from (FillType or str): :class:`~.FillType` to convert from as enum or
            string equivalent.
        fill_type_to (FillType or str): :class:`~.FillType` to convert to as enum or string
            equivalent.

    Return:
        Converted filled contour polygons.

    When converting non-chunked fill types (``FillType.OuterCode`` or ``FillType.OuterOffset``) to
    chunked ones, all polygons are placed in the first chunk. When converting in the other
    direction, all chunk information is discarded. Converting a fill type that is not aware of the
    relationship between outer boundaries and contained holes (``FillType.ChunkCombinedCode`` or
    ``FillType.ChunkCombinedOffset``) to one that is will raise a ``ValueError``.

    .. versionadded:: 1.2.0
    """
    fill_type_from = as_fill_type(fill_type_from)
    fill_type_to = as_fill_type(fill_type_to)

    check_filled(filled, fill_type_from)

    if fill_type_from == FillType.OuterCode:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_OuterCode, filled)
        return _convert_filled_from_OuterCode(filled, fill_type_to)
    elif fill_type_from == FillType.OuterOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_OuterOffset, filled)
        return _convert_filled_from_OuterOffset(filled, fill_type_to)
    elif fill_type_from == FillType.ChunkCombinedCode:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedCode, filled)
        return _convert_filled_from_ChunkCombinedCode(filled, fill_type_to)
    elif fill_type_from == FillType.ChunkCombinedOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedOffset, filled)
        return _convert_filled_from_ChunkCombinedOffset(filled, fill_type_to)
    elif fill_type_from == FillType.ChunkCombinedCodeOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedCodeOffset, filled)
        return _convert_filled_from_ChunkCombinedCodeOffset(filled, fill_type_to)
    elif fill_type_from == FillType.ChunkCombinedOffsetOffset:
        if TYPE_CHECKING:
            filled = cast(cpy.FillReturn_ChunkCombinedOffsetOffset, filled)
        return _convert_filled_from_ChunkCombinedOffsetOffset(filled, fill_type_to)
    else:
        raise ValueError(f"Invalid FillType {fill_type_from}")

