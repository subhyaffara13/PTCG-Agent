
def test_categorical_dtype(data):
    data_categorical = {
        "ordered": pd.Categorical(list("testdata") * 30, ordered=True),
        "unordered": pd.Categorical(list("testdata") * 30, ordered=False),
    }
    df = pd.DataFrame({"A": (data_categorical[data[0]])})

    with tm.assert_produces_warning(match="Interchange"):
        col = df.__dataframe__().get_column_by_name("A")
    assert col.dtype[0] == DtypeKind.CATEGORICAL
    assert col.null_count == 0
    assert col.describe_null == (ColumnNullType.USE_SENTINEL, -1)
    assert col.num_chunks() == 1
    desc_cat = col.describe_categorical
    assert desc_cat["is_ordered"] == data[1]
    assert desc_cat["is_dictionary"] is True
    assert isinstance(desc_cat["categories"], PandasColumn)
    tm.assert_series_equal(
        desc_cat["categories"]._col, pd.Series(["a", "d", "e", "s", "t"])
    )

    with tm.assert_produces_warning(match="Interchange"):
        tm.assert_frame_equal(df, from_dataframe(df.__dataframe__()))


def test_categorical_dtype(all_parsers, dtype):
    # see gh-10153
    parser = all_parsers
    data = """a,b,c
1,a,3.4
1,a,3.4
2,b,4.5"""
    expected = DataFrame(
        {
            "a": Categorical(["1", "1", "2"]),
            "b": Categorical(["a", "a", "b"]),
            "c": Categorical(["3.4", "3.4", "4.5"]),
        }
    )
    actual = parser.read_csv(StringIO(data), dtype=dtype)
    tm.assert_frame_equal(actual, expected)


def test_categorical_dtype(dtypes, exp_type):
    assert find_common_type(dtypes) == exp_type

