
def test_readjson_chunks_multiple_empty_lines(chunksize):
    j = """

    {"A":1,"B":4}



    {"A":2,"B":5}







    {"A":3,"B":6}
    """
    orig = DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    test = read_json(StringIO(j), lines=True, chunksize=chunksize)
    if chunksize is not None:
        with test:
            test = pd.concat(test)
    tm.assert_frame_equal(orig, test, obj=f"chunksize: {chunksize}")

