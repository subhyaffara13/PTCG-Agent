
def type_index_constructor(context):
    def typer(data, hashmap=None):
        if isinstance(data, types.Array):
            assert data.layout == "C"
            assert data.ndim == 1
            assert hashmap is None or isinstance(hashmap, types.DictType)
            return IndexType(data.dtype, layout=data.layout, pyclass=Index)

    return typer

