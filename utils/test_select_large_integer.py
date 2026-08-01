
def test_select_large_integer(temp_hdfstore):
    df = DataFrame(
        zip(
            ["a", "b", "c", "d"],
            [-9223372036854775801, -9223372036854775802, -9223372036854775803, 123],
        ),
        columns=["x", "y"],
    )
    temp_hdfstore.append("data", df, data_columns=True, index=False)
    result = (
        temp_hdfstore.select("data", where="y==-9223372036854775801").get("y").get(0)
    )
    expected = df["y"][0]

    assert expected == result

