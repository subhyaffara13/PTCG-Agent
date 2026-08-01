
def test_readjson_chunks(request, lines_json_df, chunksize, buffer, engine):
    # Basic test that read_json(chunks=True) gives the same result as
    # read_json(chunks=False)
    # GH17048: memory usage when lines=True
    # GH#28906: read binary json lines in chunks

    if buffer == BytesIO:
        lines_json_df = lines_json_df.encode()

    if engine == "pyarrow":
        # GH 48893
        reason = (
            "Pyarrow only supports a file path as an input and line delimited json"
            "and doesn't support chunksize parameter."
        )
        request.applymarker(pytest.mark.xfail(reason=reason, raises=ValueError))

    unchunked = read_json(buffer(lines_json_df), lines=True)
    with (
        buffer(lines_json_df) as buf,
        read_json(buf, lines=True, chunksize=chunksize, engine=engine) as reader,
    ):
        chunked = pd.concat(reader)

    tm.assert_frame_equal(chunked, unchunked)

