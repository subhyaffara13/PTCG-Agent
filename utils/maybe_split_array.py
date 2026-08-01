
def maybe_split_array(arr, chunked):
    if not chunked:
        return arr
    elif arr.dtype.storage != "pyarrow":
        return arr

    pa = pytest.importorskip("pyarrow")

    arrow_array = arr._pa_array
    split = len(arrow_array) // 2
    arrow_array = pa.chunked_array(
        [*arrow_array[:split].chunks, *arrow_array[split:].chunks]
    )
    assert arrow_array.num_chunks == 2
    return arr._from_pyarrow_array(arrow_array)

