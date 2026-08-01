
def test_api_get_schema_keys(conn, request, test_frame1):
    if "adbc" in conn:
        request.node.add_marker(
            pytest.mark.xfail(
                reason="'get_schema' not implemented for ADBC drivers",
                strict=True,
            )
        )
    conn_name = conn
    conn = request.getfixturevalue(conn)
    frame = DataFrame({"Col1": [1.1, 1.2], "Col2": [2.1, 2.2]})
    create_sql = sql.get_schema(frame, "test", con=conn, keys="Col1")

    if "mysql" in conn_name:
        constraint_sentence = "CONSTRAINT test_pk PRIMARY KEY (`Col1`)"
    else:
        constraint_sentence = 'CONSTRAINT test_pk PRIMARY KEY ("Col1")'
    assert constraint_sentence in create_sql

    # multiple columns as key (GH10385)
    create_sql = sql.get_schema(test_frame1, "test", con=conn, keys=["A", "B"])
    if "mysql" in conn_name:
        constraint_sentence = "CONSTRAINT test_pk PRIMARY KEY (`A`, `B`)"
    else:
        constraint_sentence = 'CONSTRAINT test_pk PRIMARY KEY ("A", "B")'
    assert constraint_sentence in create_sql

