
def test_assert_frame_equal_check_like_categorical_midx():
    # GH#48975
    left = DataFrame(
        [[1], [2], [3]],
        index=pd.MultiIndex.from_arrays(
            [
                pd.Categorical(["a", "b", "c"]),
                pd.Categorical(["a", "b", "c"]),
            ]
        ),
    )
    right = DataFrame(
        [[3], [2], [1]],
        index=pd.MultiIndex.from_arrays(
            [
                pd.Categorical(["c", "b", "a"]),
                pd.Categorical(["c", "b", "a"]),
            ]
        ),
    )
    tm.assert_frame_equal(left, right, check_like=True)

