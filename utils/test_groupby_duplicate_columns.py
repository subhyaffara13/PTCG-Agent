
def test_groupby_duplicate_columns(infer_string):
    # GH: 31735
    if infer_string:
        pytest.importorskip("pyarrow")
    df = DataFrame(
        {"A": ["f", "e", "g", "h"], "B": ["a", "b", "c", "d"], "C": [1, 2, 3, 4]}
    ).astype(object)
    df.columns = ["A", "B", "B"]
    with pd.option_context("future.infer_string", infer_string):
        result = df.groupby([0, 0, 0, 0]).min()
    expected = DataFrame(
        [["e", "a", 1]], index=np.array([0]), columns=["A", "B", "B"], dtype=object
    )
    tm.assert_frame_equal(result, expected)

