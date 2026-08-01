
def test_lambda_named_agg(func):
    # see gh-28467
    animals = DataFrame(
        {
            "kind": ["cat", "dog", "cat", "dog"],
            "height": [9.1, 6.0, 9.5, 34.0],
            "weight": [7.9, 7.5, 9.9, 198.0],
        }
    )

    result = animals.groupby("kind").agg(
        mean_height=("height", "mean"), perc90=("height", func)
    )
    expected = DataFrame(
        [[9.3, 9.1036], [20.0, 6.252]],
        columns=["mean_height", "perc90"],
        index=Index(["cat", "dog"], name="kind"),
    )

    tm.assert_frame_equal(result, expected)

