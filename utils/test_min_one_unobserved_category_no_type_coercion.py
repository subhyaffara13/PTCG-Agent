
def test_min_one_unobserved_category_no_type_coercion(dtype):
    # GH#58084
    df = DataFrame({"A": Categorical([1, 1, 2], categories=[1, 2, 3]), "B": [3, 4, 5]})
    df["B"] = df["B"].astype(dtype)
    gb = df.groupby("A", observed=False)
    result = gb.transform("min")

    expected = DataFrame({"B": [3, 3, 5]}, dtype=dtype)
    tm.assert_frame_equal(expected, result)

