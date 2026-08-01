
def test_json_roundtrip_string_inference(orient):
    df = DataFrame(
        [["a", "b"], ["c", "d"]], index=["row 1", "row 2"], columns=["col 1", "col 2"]
    )
    out = df.to_json()
    with pd.option_context("future.infer_string", True):
        result = read_json(StringIO(out))
    dtype = pd.StringDtype(na_value=np.nan)
    expected = DataFrame(
        [["a", "b"], ["c", "d"]],
        dtype=dtype,
        index=Index(["row 1", "row 2"], dtype=dtype),
        columns=Index(["col 1", "col 2"], dtype=dtype),
    )
    tm.assert_frame_equal(result, expected)

