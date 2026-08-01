
def test_dataframe_to_sql_arrow_dtypes(conn, request):
    # GH 52046
    pytest.importorskip("pyarrow")
    df = DataFrame(
        {
            "int": pd.array([1], dtype="int8[pyarrow]"),
            "datetime": pd.array(
                [datetime(2023, 1, 1)], dtype="timestamp[ns][pyarrow]"
            ),
            "date": pd.array([date(2023, 1, 1)], dtype="date32[day][pyarrow]"),
            "timedelta": pd.array([timedelta(1)], dtype="duration[ns][pyarrow]"),
            "string": pd.array(["a"], dtype="string[pyarrow]"),
        }
    )

    if "adbc" in conn:
        if conn == "sqlite_adbc_conn":
            df = df.drop(columns=["timedelta"])
        if pa_version_under14p1:
            exp_warning = DeprecationWarning
            msg = "is_sparse is deprecated"
        else:
            exp_warning = None
            msg = ""
    else:
        exp_warning = UserWarning
        msg = "the 'timedelta'"

    conn = request.getfixturevalue(conn)
    with tm.assert_produces_warning(exp_warning, match=msg, check_stacklevel=False):
        df.to_sql(name="test_arrow", con=conn, if_exists="replace", index=False)

