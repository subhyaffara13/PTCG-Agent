
def test_api_complex_raises(conn, request):
    conn_name = conn
    conn = request.getfixturevalue(conn)
    df = DataFrame({"a": [1 + 1j, 2j]})

    if "adbc" in conn_name:
        msg = "datatypes not supported"
    else:
        msg = "Complex datatypes not supported"
    with pytest.raises(ValueError, match=msg):
        assert df.to_sql("test_complex", con=conn) is None

