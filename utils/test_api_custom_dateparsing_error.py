
def test_api_custom_dateparsing_error(
    conn, request, read_sql, text, mode, error, types_data_frame
):
    conn_name = conn
    conn = request.getfixturevalue(conn)
    if text == "types" and conn_name == "sqlite_buildin_types":
        request.applymarker(
            pytest.mark.xfail(reason="failing combination of arguments")
        )

    expected = types_data_frame.astype({"DateCol": "datetime64[us]"})

    result = read_sql(
        text,
        con=conn,
        parse_dates={
            "DateCol": {"errors": error},
        },
    )
    if "postgres" in conn_name:
        # TODO: clean up types_data_frame fixture
        result["BoolCol"] = result["BoolCol"].astype(int)
        result["BoolColWithNull"] = result["BoolColWithNull"].astype(float)

    if conn_name == "postgresql_adbc_types":
        expected = expected.astype(
            {
                "IntDateCol": "int32",
                "IntDateOnlyCol": "int32",
                "IntCol": "int32",
            }
        )

    tm.assert_frame_equal(result, expected)

