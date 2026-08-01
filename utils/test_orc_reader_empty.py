
def test_orc_reader_empty(dirpath, using_infer_string):
    columns = [
        "boolean1",
        "byte1",
        "short1",
        "int1",
        "long1",
        "float1",
        "double1",
        "bytes1",
        "string1",
    ]
    dtypes = [
        "bool",
        "int8",
        "int16",
        "int32",
        "int64",
        "float32",
        "float64",
        "object",
        "str" if using_infer_string else "object",
    ]
    expected = pd.DataFrame(index=pd.RangeIndex(0))
    for colname, dtype in zip(columns, dtypes, strict=True):
        expected[colname] = pd.Series(dtype=dtype)
    expected.columns = expected.columns.astype("str")

    inputfile = os.path.join(dirpath, "TestOrcFile.emptyFile.orc")
    got = read_orc(inputfile, columns=columns)

    tm.assert_equal(expected, got)

