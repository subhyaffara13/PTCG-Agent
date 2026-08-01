
def test_string(value: t.Any) -> bool:
    """Return true if the object is a string."""
    return isinstance(value, str)


def test_string():
    string_data = {
        "separator data": [
            "abC|DeF,Hik",
            "234,3245.67",
            "gSaf,qWer|Gre",
            "asd3,4sad|",
            np.nan,
        ]
    }
    test_str_data = string_data["separator data"] + [""]
    df = pd.DataFrame({"A": test_str_data})
    with tm.assert_produces_warning(match="Interchange"):
        col = df.__dataframe__().get_column_by_name("A")

    assert col.size() == 6
    assert col.null_count == 1
    assert col.dtype[0] == DtypeKind.STRING
    assert col.describe_null == (ColumnNullType.USE_BYTEMASK, 0)

    df_sliced = df[1:]
    with tm.assert_produces_warning(match="Interchange"):
        col = df_sliced.__dataframe__().get_column_by_name("A")
    assert col.size() == 5
    assert col.null_count == 1
    assert col.dtype[0] == DtypeKind.STRING
    assert col.describe_null == (ColumnNullType.USE_BYTEMASK, 0)

