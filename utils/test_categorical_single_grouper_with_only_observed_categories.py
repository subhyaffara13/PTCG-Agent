
def test_categorical_single_grouper_with_only_observed_categories(
    education_df, as_index, observed, normalize, name, expected_data, request
):
    # Test single categorical grouper with only observed grouping categories
    # when non-groupers are also categorical
    request.applymarker(
        pytest.mark.xfail(
            reason=(
                "pandas default unstable sorting of duplicates"
                "issue with numpy>=1.25 with AVX instructions"
            ),
            strict=False,
        )
    )

    gp = education_df.astype("category").groupby(
        "country", as_index=as_index, observed=observed
    )
    result = gp.value_counts(normalize=normalize)

    expected_index = MultiIndex.from_tuples(
        [
            ("FR", "male", "low"),
            ("FR", "male", "medium"),
            ("FR", "female", "high"),
            ("FR", "male", "high"),
            ("FR", "female", "low"),
            ("FR", "female", "medium"),
            ("US", "male", "low"),
            ("US", "female", "high"),
            ("US", "male", "medium"),
            ("US", "male", "high"),
            ("US", "female", "low"),
            ("US", "female", "medium"),
        ],
        names=["country", "gender", "education"],
    )

    expected_series = Series(
        data=expected_data,
        index=expected_index,
        name=name,
    )
    for i in range(3):
        expected_series.index = expected_series.index.set_levels(
            CategoricalIndex(expected_series.index.levels[i]), level=i
        )

    if as_index:
        tm.assert_series_equal(result, expected_series)
    else:
        expected = expected_series.reset_index(
            name="proportion" if normalize else "count"
        )
        tm.assert_frame_equal(result, expected)

