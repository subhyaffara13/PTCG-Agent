
def test_double_precision(conn, request):
    if conn == "sqlite_str":
        pytest.skip("sqlite_str has no inspection system")

    conn = request.getfixturevalue(conn)

    from sqlalchemy import (
        BigInteger,
        Float,
        Integer,
    )
    from sqlalchemy.schema import MetaData

    V = 1.23456789101112131415

    df = DataFrame(
        {
            "f32": Series([V], dtype="float32"),
            "f64": Series([V], dtype="float64"),
            "f64_as_f32": Series([V], dtype="float64"),
            "i32": Series([5], dtype="int32"),
            "i64": Series([5], dtype="int64"),
        }
    )

    assert (
        df.to_sql(
            name="test_dtypes",
            con=conn,
            index=False,
            if_exists="replace",
            dtype={"f64_as_f32": Float(precision=23)},
        )
        == 1
    )
    res = sql.read_sql_table("test_dtypes", conn)

    # check precision of float64
    assert np.round(df["f64"].iloc[0], 14) == np.round(res["f64"].iloc[0], 14)

    # check sql types
    meta = MetaData()
    meta.reflect(bind=conn)
    col_dict = meta.tables["test_dtypes"].columns
    assert str(col_dict["f32"].type) == str(col_dict["f64_as_f32"].type)
    assert isinstance(col_dict["f32"].type, Float)
    assert isinstance(col_dict["f64"].type, Float)
    assert isinstance(col_dict["i32"].type, Integer)
    assert isinstance(col_dict["i64"].type, BigInteger)

