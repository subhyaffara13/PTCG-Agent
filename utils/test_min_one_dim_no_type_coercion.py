
def test_min_one_dim_no_type_coercion():
    # GH#58084
    df = DataFrame({"Y": [9435, -5465765, 5055, 0, 954960]})
    df["Y"] = df["Y"].astype("int32")
    categories = Categorical([1, 2, 2, 5, 1], categories=[1, 2, 3, 4, 5])

    gb = df.groupby(categories, observed=False)
    result = gb.transform("min")

    expected = DataFrame({"Y": [9435, -5465765, -5465765, 0, 9435]}, dtype="int32")
    tm.assert_frame_equal(expected, result)

