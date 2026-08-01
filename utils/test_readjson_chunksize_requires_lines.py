
def test_readjson_chunksize_requires_lines(lines_json_df, engine):
    msg = "chunksize can only be passed if lines=True"
    with pytest.raises(ValueError, match=msg):
        with read_json(
            StringIO(lines_json_df), lines=False, chunksize=2, engine=engine
        ) as _:
            pass

