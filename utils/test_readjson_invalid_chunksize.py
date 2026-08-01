
def test_readjson_invalid_chunksize(lines_json_df, chunksize, engine):
    msg = r"'chunksize' must be an integer >=1"

    with pytest.raises(ValueError, match=msg):
        with read_json(
            StringIO(lines_json_df), lines=True, chunksize=chunksize, engine=engine
        ) as _:
            pass

