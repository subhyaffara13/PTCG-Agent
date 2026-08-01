
def test_mixed_dtypes(df_from_dict):
    df = df_from_dict(
        {
            "a": [1, 2, 3],  # dtype kind INT = 0
            "b": [3, 4, 5],  # dtype kind INT = 0
            "c": [1.5, 2.5, 3.5],  # dtype kind FLOAT = 2
            "d": [9, 10, 11],  # dtype kind INT = 0
            "e": [True, False, True],  # dtype kind BOOLEAN = 20
            "f": ["a", "", "c"],  # dtype kind STRING = 21
        }
    )
    with tm.assert_produces_warning(match="Interchange"):
        dfX = df.__dataframe__()
    # for meanings of dtype[0] see the spec; we cannot import the spec here as this
    # file is expected to be vendored *anywhere*;
    # values for dtype[0] are explained above
    columns = {"a": 0, "b": 0, "c": 2, "d": 0, "e": 20, "f": 21}

    for column, kind in columns.items():
        colX = dfX.get_column_by_name(column)
        assert colX.null_count == 0
        assert isinstance(colX.null_count, int)
        assert colX.size() == 3
        assert colX.offset == 0

        assert colX.dtype[0] == kind

    assert dfX.get_column_by_name("c").dtype[1] == 64

