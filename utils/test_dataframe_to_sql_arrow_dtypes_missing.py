
def test_dataframe_to_sql_arrow_dtypes_missing(conn, request, nulls_fixture):
    # GH 52046
    pytest.importorskip("pyarrow")
    if isinstance(nulls_fixture, Decimal):
        pytest.skip(
            # GH#61773
            reason="Decimal('NaN') not supported in constructor for timestamp dtype"
        )

    df = DataFrame(
        {
            "datetime": pd.array(
                [datetime(2023, 1, 1), nulls_fixture], dtype="timestamp[ns][pyarrow]"
            ),
        }
    )
    conn = request.getfixturevalue(conn)
    df.to_sql(name="test_arrow", con=conn, if_exists="replace", index=False)

