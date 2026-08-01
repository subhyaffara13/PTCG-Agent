
def test_buffer(method):
    # Smoke test that sparse matrices with read-only buffers (e.g., those from
    # joblib workers) do not cause::
    #
    #     ValueError: buffer source array is read-only
    #
    G = scipy.sparse.csr_array([[1.]])
    G.data.flags['WRITEABLE'] = False
    shortest_path(G, method=method)


def test_buffer(df_from_dict):
    arr = [0, 1, -1]
    df = df_from_dict({"a": arr})
    with tm.assert_produces_warning(match="Interchange"):
        dfX = df.__dataframe__()
    colX = dfX.get_column(0)
    bufX = colX.get_buffers()

    dataBuf, dataDtype = bufX["data"]

    assert dataBuf.bufsize > 0
    assert dataBuf.ptr != 0
    device, _ = dataBuf.__dlpack_device__()

    # for meanings of dtype[0] see the spec; we cannot import the spec here as this
    # file is expected to be vendored *anywhere*
    assert dataDtype[0] == 0  # INT

    if device == 1:  # CPU-only as we're going to directly read memory here
        bitwidth = dataDtype[1]
        ctype = {
            8: ctypes.c_int8,
            16: ctypes.c_int16,
            32: ctypes.c_int32,
            64: ctypes.c_int64,
        }[bitwidth]

        for idx, truth in enumerate(arr):
            val = ctype.from_address(dataBuf.ptr + idx * (bitwidth // 8)).value
            assert val == truth, f"Buffer at index {idx} mismatch"

