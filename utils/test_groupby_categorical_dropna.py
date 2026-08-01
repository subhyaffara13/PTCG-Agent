
def test_groupby_categorical_dropna(observed, dropna):
    # GH#48645 - dropna should have no impact on the result when there are no NA values
    cat = Categorical([1, 2], categories=[1, 2, 3])
    df = DataFrame({"x": Categorical([1, 2], categories=[1, 2, 3]), "y": [3, 4]})
    gb = df.groupby("x", observed=observed, dropna=dropna)
    result = gb.sum()

    if observed:
        expected = DataFrame({"y": [3, 4]}, index=cat)
    else:
        index = CategoricalIndex([1, 2, 3], [1, 2, 3])
        expected = DataFrame({"y": [3, 4, 0]}, index=index)
    expected.index.name = "x"

    tm.assert_frame_equal(result, expected)

