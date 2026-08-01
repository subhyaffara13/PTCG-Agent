
def test_categorical_non_groupers(
    education_df, as_index, observed, normalize, name, expected_data, request
):
    # GH#46357 Test non-observed categories are included in the result,
    # regardless of `observed`

    request.applymarker(
        pytest.mark.xfail(
            reason=(
                "pandas default unstable sorting of duplicates"
                "issue with numpy>=1.25 with AVX instructions"
            ),
            strict=False,
        )
    )

    education_df = education_df.copy()
    education_df["gender"] = education_df["gender"].astype("category")
    education_df["education"] = education_df["education"].astype("category")

    gp = education_df.groupby("country", as_index=as_index, observed=observed)
    result = gp.value_counts(normalize=normalize)

    expected_index = [
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
    ]
    expected_series = Series(
        data=expected_data,
        index=MultiIndex.from_tuples(
            expected_index,
            names=["country", "gender", "education"],
        ),
        name=name,
    )
    for i in range(1, 3):
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

