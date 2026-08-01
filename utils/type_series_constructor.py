
def type_series_constructor(context):
    def typer(data, index, name=None):
        if isinstance(index, IndexType) and isinstance(data, types.Array):
            assert data.ndim == 1
            if name is None:
                name = types.intp
            return SeriesType(data.dtype, index, name)

    return typer

