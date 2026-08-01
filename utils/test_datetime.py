
def test_datetime():
    # GH9049: ensure backward compatibility
    levels = pd.date_range("2014-01-01", periods=4)
    codes = np.random.default_rng(2).integers(0, 4, size=10)

    cats = Categorical.from_codes(codes, levels, ordered=True)

    data = DataFrame(np.random.default_rng(2).standard_normal((10, 4)))
    result = data.groupby(cats, observed=False).mean()

    expected = data.groupby(np.asarray(cats), observed=False).mean()
    expected = expected.reindex(levels)
    expected.index = CategoricalIndex(
        expected.index, categories=expected.index, ordered=True
    )

    tm.assert_frame_equal(result, expected)

    grouped = data.groupby(cats, observed=False)
    desc_result = grouped.describe()

    idx = cats.codes.argsort()
    ord_labels = cats.take(idx)
    ord_data = data.take(idx)
    expected = ord_data.groupby(ord_labels, observed=False).describe()
    tm.assert_frame_equal(desc_result, expected)
    tm.assert_index_equal(desc_result.index, expected.index)
    tm.assert_index_equal(
        desc_result.index.get_level_values(0), expected.index.get_level_values(0)
    )

    # GH 10460
    expc = Categorical.from_codes(np.arange(4).repeat(8), levels, ordered=True)
    exp = CategoricalIndex(expc)
    tm.assert_index_equal((desc_result.stack().index.get_level_values(0)), exp)
    exp = Index(["count", "mean", "std", "min", "25%", "50%", "75%", "max"] * 4)
    tm.assert_index_equal((desc_result.stack().index.get_level_values(1)), exp)


def test_datetime():
    df = pd.DataFrame({"A": [pd.Timestamp("2022-01-01"), pd.NaT]})
    with tm.assert_produces_warning(match="Interchange"):
        col = df.__dataframe__().get_column_by_name("A")

    assert col.size() == 2
    assert col.null_count == 1
    assert col.dtype[0] == DtypeKind.DATETIME
    assert col.describe_null == (ColumnNullType.USE_SENTINEL, iNaT)

    with tm.assert_produces_warning(match="Interchange"):
        tm.assert_frame_equal(df, from_dataframe(df.__dataframe__()))


def test_datetime(conn, request):
    conn_name = conn
    conn = request.getfixturevalue(conn)
    df = DataFrame(
        {"A": date_range("2013-01-01 09:00:00", periods=3), "B": np.arange(3.0)}
    )
    assert df.to_sql(name="test_datetime", con=conn) == 3

    # with read_table -> type information from schema used
    result = sql.read_sql_table("test_datetime", conn)
    result = result.drop("index", axis=1)

    expected = df[:]
    expected["A"] = expected["A"].astype("M8[us]")
    tm.assert_frame_equal(result, expected)

    # with read_sql -> no type information -> sqlite has no native
    result = sql.read_sql_query("SELECT * FROM test_datetime", conn)
    result = result.drop("index", axis=1)
    if "sqlite" in conn_name:
        assert isinstance(result.loc[0, "A"], str)
        result["A"] = to_datetime(result["A"])
    tm.assert_frame_equal(result, expected)

