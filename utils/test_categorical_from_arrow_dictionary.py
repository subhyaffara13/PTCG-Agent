
def test_categorical_from_arrow_dictionary():
    # GH 60563
    df = pd.DataFrame(
        {"A": ["a1", "a2"]}, dtype=ArrowDtype(pa.dictionary(pa.int32(), pa.utf8()))
    )
    result = df.value_counts(dropna=False)
    expected = pd.Series(
        [1, 1],
        index=pd.MultiIndex.from_arrays(
            [pd.Index(["a1", "a2"], dtype=ArrowDtype(pa.string()), name="A")]
        ),
        name="count",
        dtype="int64",
    )
    tm.assert_series_equal(result, expected)

