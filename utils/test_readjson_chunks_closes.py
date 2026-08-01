
def test_readjson_chunks_closes(chunksize, temp_file):
    df = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df.to_json(temp_file, lines=True, orient="records")
    reader = JsonReader(
        temp_file,
        orient=None,
        typ="frame",
        dtype=True,
        convert_axes=True,
        convert_dates=True,
        keep_default_dates=True,
        precise_float=False,
        date_unit=None,
        encoding=None,
        lines=True,
        chunksize=chunksize,
        compression=None,
        nrows=None,
    )
    with reader:
        reader.read()
    assert reader.handles.handle.closed, (
        f"didn't close stream with chunksize = {chunksize}"
    )

