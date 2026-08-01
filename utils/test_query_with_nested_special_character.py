
def test_query_with_nested_special_character(temp_hdfstore):
    df = DataFrame(
        {
            "a": ["a", "a", "c", "b", "test & test", "c", "b", "e"],
            "b": [1, 2, 3, 4, 5, 6, 7, 8],
        }
    )
    expected = df[df.a == "test & test"]
    temp_hdfstore.append("test", df, format="table", data_columns=True)
    result = temp_hdfstore.select("test", 'a = "test & test"')
    tm.assert_frame_equal(expected, result)

