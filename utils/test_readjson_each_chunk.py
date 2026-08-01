
def test_readjson_each_chunk(request, lines_json_df, engine):
    if engine == "pyarrow":
        # GH 48893
        reason = (
            "Pyarrow only supports a file path as an input and line delimited json"
            "and doesn't support chunksize parameter."
        )
        request.applymarker(pytest.mark.xfail(reason=reason, raises=ValueError))

    # Other tests check that the final result of read_json(chunksize=True)
    # is correct. This checks the intermediate chunks.
    with read_json(
        StringIO(lines_json_df), lines=True, chunksize=2, engine=engine
    ) as reader:
        chunks = list(reader)
    assert chunks[0].shape == (2, 2)
    assert chunks[1].shape == (1, 2)

