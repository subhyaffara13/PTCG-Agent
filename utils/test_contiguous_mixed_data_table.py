
def test_contiguous_mixed_data_table(start, stop, temp_hdfstore):
    # GH 17021
    df = DataFrame(
        {
            "a": Series([20111010, 20111011, 20111012]),
            "b": Series(["ab", "cd", "ab"]),
        }
    )

    temp_hdfstore.append("test_dataset", df)

    result = temp_hdfstore.select("test_dataset", start=start, stop=stop)
    tm.assert_frame_equal(df[start:stop], result)

