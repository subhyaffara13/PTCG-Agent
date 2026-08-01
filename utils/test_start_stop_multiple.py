
def test_start_stop_multiple(temp_hdfstore):
    # GH 16209
    df = DataFrame({"foo": [1, 2], "bar": [1, 2]})

    temp_hdfstore.append_to_multiple(
        {"selector": ["foo"], "data": None}, df, selector="selector"
    )
    result = temp_hdfstore.select_as_multiple(
        ["selector", "data"], selector="selector", start=0, stop=1
    )
    expected = df.loc[[0], ["foo", "bar"]]
    tm.assert_frame_equal(result, expected)

