
def test_sorted_missing_category_values():
    # GH 28597
    df = DataFrame(
        {
            "foo": [
                "small",
                "large",
                "large",
                "large",
                "medium",
                "large",
                "large",
                "medium",
            ],
            "bar": ["C", "A", "A", "C", "A", "C", "A", "C"],
        }
    )
    df["foo"] = (
        df["foo"]
        .astype("category")
        .cat.set_categories(["tiny", "small", "medium", "large"], ordered=True)
    )

    expected = DataFrame(
        {
            "tiny": {"A": 0, "C": 0},
            "small": {"A": 0, "C": 1},
            "medium": {"A": 1, "C": 1},
            "large": {"A": 3, "C": 2},
        }
    )
    expected = expected.rename_axis("bar", axis="index")
    expected.columns = CategoricalIndex(
        ["tiny", "small", "medium", "large"],
        categories=["tiny", "small", "medium", "large"],
        ordered=True,
        name="foo",
        dtype="category",
    )

    result = df.groupby(["bar", "foo"], observed=False).size().unstack()

    tm.assert_frame_equal(result, expected)

