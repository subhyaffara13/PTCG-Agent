
def test_join_multiindex_categorical_output_index_dtype(how, values):
    # GH#50906
    df1 = DataFrame(
        {
            "a": Categorical([0, 1, 2]),
            "b": Categorical([0, 1, 2]),
            "c": [0, 1, 2],
        }
    ).set_index(["a", "b"])

    df2 = DataFrame(
        {
            "a": Categorical([0, 2, 1]),
            "b": Categorical([0, 2, 1]),
            "d": [0, 2, 1],
        }
    ).set_index(["a", "b"])

    expected = DataFrame(
        {
            "a": Categorical(values),
            "b": Categorical(values),
            "c": values,
            "d": values,
        }
    ).set_index(["a", "b"])

    result = df1.join(df2, how=how)
    tm.assert_frame_equal(result, expected)

