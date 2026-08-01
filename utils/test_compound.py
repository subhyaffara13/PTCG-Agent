
def test_compound():
    assert (exp(SetExpr(Interval(0, 1))*2 + 1)).set == \
           Interval(exp(1), exp(3))


def test_compound():
    e1 = b1*A*B*k1*b2*k2*b3
    assert e1 == InnerProduct(b2, k2)*b1*A*B*OuterProduct(k1, b3)

    e2 = TensorProduct(k1, k2)*TensorProduct(b1, b2)
    assert e2 == TensorProduct(
        OuterProduct(k1, b1),
        OuterProduct(k2, b2)
    )


def test_compound(
    education_df,
    normalize,
    sort,
    ascending,
    expected_rows,
    expected_count,
    expected_group_size,
    any_string_dtype,
    using_infer_string,
):
    dtype = any_string_dtype
    education_df = education_df.astype(dtype)
    education_df.columns = education_df.columns.astype(dtype)
    # Multiple groupby keys and as_index=False
    gp = education_df.groupby(["country", "gender"], as_index=False, sort=False)
    result = gp["education"].value_counts(
        normalize=normalize, sort=sort, ascending=ascending
    )
    expected = DataFrame()
    for column in ["country", "gender", "education"]:
        expected[column] = [education_df[column][row] for row in expected_rows]
        expected = expected.astype(dtype)
        expected.columns = expected.columns.astype(dtype)
    if normalize:
        expected["proportion"] = expected_count
        expected["proportion"] /= expected_group_size
        if dtype == "string[pyarrow]":
            # TODO(nullable) also string[python] should return nullable dtypes
            expected["proportion"] = expected["proportion"].convert_dtypes()
    else:
        expected["count"] = expected_count
        if dtype == "string[pyarrow]":
            expected["count"] = expected["count"].convert_dtypes()
    if using_infer_string and dtype == object:
        expected = expected.astype(
            {"country": "str", "gender": "str", "education": "str"}
        )

    tm.assert_frame_equal(result, expected)

