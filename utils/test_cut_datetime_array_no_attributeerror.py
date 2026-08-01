
def test_cut_datetime_array_no_attributeerror():
    # GH 55431
    ser = Series(to_datetime(["2023-10-06 12:00:00+0000", "2023-10-07 12:00:00+0000"]))

    result = cut(ser.array, bins=2)

    categories = result.categories
    expected = Categorical.from_codes([0, 1], categories=categories, ordered=True)

    tm.assert_categorical_equal(
        result, expected, check_dtype=True, check_category_order=True
    )

