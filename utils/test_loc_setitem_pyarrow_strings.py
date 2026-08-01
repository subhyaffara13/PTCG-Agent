
def test_loc_setitem_pyarrow_strings():
    # GH#52319
    pytest.importorskip("pyarrow")
    df = DataFrame(
        {
            "strings": Series(["A", "B", "C"], dtype="string[pyarrow]"),
            "ids": Series([True, True, False]),
        }
    )
    new_value = Series(["X", "Y"])
    df.loc[df.ids, "strings"] = new_value

    expected_df = DataFrame(
        {
            "strings": Series(["X", "Y", "C"], dtype="string[pyarrow]"),
            "ids": Series([True, True, False]),
        }
    )

    tm.assert_frame_equal(df, expected_df)

