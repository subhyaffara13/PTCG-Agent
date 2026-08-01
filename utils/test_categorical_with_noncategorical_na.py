
def test_categorical_with_noncategorical_na(observed, sort):
    # https://github.com/pandas-dev/pandas/issues/63920
    df = DataFrame(
        {
            "dates": list("YXXYY"),
            "sector": Categorical(
                [2, 1, 2, 1, np.nan], categories=[1, 2, 3], ordered=True
            ),
            "metric": [1, 2, 3, 4, 5],
        }
    )
    gb = df.groupby(["dates", "sector"], observed=observed, sort=sort)
    # Only testing the ids/result_index, okay to just use one kernel
    result = gb.sum()

    if sort and observed:
        taker = [0, 1, 2, 3]
    elif not sort and observed:
        taker = [3, 0, 1, 2]
    elif sort and not observed:
        taker = [0, 1, 4, 2, 3, 5]
    elif not sort and not observed:
        taker = [3, 0, 1, 2, 5, 4]
    expected = (
        DataFrame(
            {
                "dates": list("XXYYXY"),
                "sector": Categorical(
                    [1, 2, 1, 2, 3, 3], categories=[1, 2, 3], ordered=True
                ),
                "metric": [2, 3, 4, 1, 0, 0],
            }
        )
        .set_index(["dates", "sector"])
        .take(taker)
    )
    tm.assert_frame_equal(result, expected)

