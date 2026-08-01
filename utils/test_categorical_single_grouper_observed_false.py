
def test_categorical_single_grouper_observed_false(
    education_df, as_index, normalize, name, expected_data, request
):
    # GH#46357

    request.applymarker(
        pytest.mark.xfail(
            reason=(
                "pandas default unstable sorting of duplicates"
                "issue with numpy>=1.25 with AVX instructions"
            ),
            strict=False,
        )
    )

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
        ("ASIA", "male", "low"),
        ("ASIA", "male", "medium"),
        ("ASIA", "male", "high"),
        ("ASIA", "female", "low"),
        ("ASIA", "female", "medium"),
        ("ASIA", "female", "high"),
    ]

    assert_categorical_single_grouper(
        education_df=education_df,
        as_index=as_index,
        observed=False,
        expected_index=expected_index,
        normalize=normalize,
        name=name,
        expected_data=expected_data,
    )

