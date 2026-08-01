
def test_min_all_empty_data_no_type_coercion():
    # GH#58084
    df = DataFrame(
        {
            "X": Categorical(
                [],
                categories=[1, "randomcat", 100],
            ),
            "Y": [],
        }
    )
    df["Y"] = df["Y"].astype("int32")

    gb = df.groupby("X", observed=False)
    result = gb.transform("min")

    expected = DataFrame({"Y": []}, dtype="int32")
    tm.assert_frame_equal(expected, result)

