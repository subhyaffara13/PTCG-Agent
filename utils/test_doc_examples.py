
def test_doc_examples():
    # Test the examples in the documentation
    df = pd.DataFrame(
        [["a", 1], ["a", 2], ["a", 3], ["b", 4], ["b", 5]], columns=["A", "B"]
    )

    grouped = df.groupby("A", as_index=False)

    result = grouped._positional_selector[1:2]
    expected = pd.DataFrame([["a", 2], ["b", 5]], columns=["A", "B"], index=[1, 4])

    tm.assert_frame_equal(result, expected)

    result = grouped._positional_selector[1, -1]
    expected = pd.DataFrame(
        [["a", 2], ["a", 3], ["b", 5]], columns=["A", "B"], index=[1, 2, 4]
    )

    tm.assert_frame_equal(result, expected)

