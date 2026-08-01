
def test_dataframe(data):
    NCOLS, NROWS = 10, 20
    data = {
        f"col{int((i - NCOLS / 2) % NCOLS + 1)}": [data() for _ in range(NROWS)]
        for i in range(NCOLS)
    }
    df = pd.DataFrame(data)

    with tm.assert_produces_warning(match="Interchange"):
        df2 = df.__dataframe__()

    assert df2.num_columns() == NCOLS
    assert df2.num_rows() == NROWS

    assert list(df2.column_names()) == list(data.keys())

    indices = (0, 2)
    names = tuple(list(data.keys())[idx] for idx in indices)

    with tm.assert_produces_warning(match="Interchange"):
        result = from_dataframe(df2.select_columns(indices))
        expected = from_dataframe(df2.select_columns_by_name(names))
    tm.assert_frame_equal(result, expected)

    assert isinstance(result.attrs["_INTERCHANGE_PROTOCOL_BUFFERS"], list)
    assert isinstance(expected.attrs["_INTERCHANGE_PROTOCOL_BUFFERS"], list)


def test_dataframe(df_from_dict):
    df = df_from_dict(
        {"x": [True, True, False], "y": [1, 2, 0], "z": [9.2, 10.5, 11.8]}
    )
    with tm.assert_produces_warning(match="Interchange"):
        dfX = df.__dataframe__()

    assert dfX.num_columns() == 3
    assert dfX.num_rows() == 3
    assert dfX.num_chunks() == 1
    assert list(dfX.column_names()) == ["x", "y", "z"]
    assert list(dfX.select_columns((0, 2)).column_names()) == list(
        dfX.select_columns_by_name(("x", "z")).column_names()
    )

