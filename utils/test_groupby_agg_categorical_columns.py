
def test_groupby_agg_categorical_columns(func, expected_values):
    # 31256
    df = DataFrame(
        {
            "id": [0, 1, 2, 3, 4],
            "groups": [0, 1, 1, 2, 2],
            "value": Categorical([0, 0, 0, 0, 1]),
        }
    ).set_index("id")
    result = df.groupby("groups").agg(func)

    expected = DataFrame(
        {"value": expected_values}, index=Index([0, 1, 2], name="groups")
    )
    tm.assert_frame_equal(result, expected)

