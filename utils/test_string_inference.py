
def test_string_inference(temp_file):
    # GH#54431
    df = pd.DataFrame(data={"a": ["x", "y"]})
    df.to_orc(temp_file)
    with pd.option_context("future.infer_string", True):
        result = read_orc(temp_file)
    expected = pd.DataFrame(
        data={"a": ["x", "y"]},
        dtype=pd.StringDtype(na_value=np.nan),
        columns=pd.Index(["a"], dtype=pd.StringDtype(na_value=np.nan)),
    )
    tm.assert_frame_equal(result, expected)


def test_string_inference(all_parsers):
    # GH#54430
    dtype = pd.StringDtype(na_value=np.nan)

    data = """a,b
x,1
y,2
,3"""
    parser = all_parsers
    with pd.option_context("future.infer_string", True):
        result = parser.read_csv(StringIO(data))

    expected = DataFrame(
        {"a": pd.Series(["x", "y", None], dtype=dtype), "b": [1, 2, 3]},
        columns=pd.Index(["a", "b"], dtype=dtype),
    )
    tm.assert_frame_equal(result, expected)

