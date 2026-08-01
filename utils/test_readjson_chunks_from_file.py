
def test_readjson_chunks_from_file(request, engine, temp_file):
    if engine == "pyarrow":
        # GH 48893
        reason = (
            "Pyarrow only supports a file path as an input and line delimited json"
            "and doesn't support chunksize parameter."
        )
        request.applymarker(pytest.mark.xfail(reason=reason, raises=ValueError))

    df = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df.to_json(temp_file, lines=True, orient="records")
    with read_json(temp_file, lines=True, chunksize=1, engine=engine) as reader:
        chunked = pd.concat(reader)
    unchunked = read_json(temp_file, lines=True, engine=engine)
    tm.assert_frame_equal(unchunked, chunked)

