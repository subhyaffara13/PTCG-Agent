
def test_roundtrip(cls_name):
    cls = getattr(m, cls_name)
    p = cls("test_value")
    p.setExtra1(15)
    p.setExtra2(48)

    data = pickle.dumps(p, 2)  # Must use pickle protocol >= 2
    p2 = pickle.loads(data)
    assert p2.value() == p.value()
    assert p2.extra1() == p.extra1()
    assert p2.extra2() == p.extra2()


def test_roundtrip(conn, request, test_frame1):
    if conn == "sqlite_str":
        pytest.skip("sqlite_str has no inspection system")

    conn_name = conn
    conn = request.getfixturevalue(conn)
    with pandasSQL_builder(conn) as pandasSQL:
        with pandasSQL.run_transaction():
            assert pandasSQL.to_sql(test_frame1, "test_frame_roundtrip") == 4
            result = pandasSQL.read_query("SELECT * FROM test_frame_roundtrip")

    if "adbc" in conn_name:
        result = result.rename(columns={"__index_level_0__": "level_0"})
    result.set_index("level_0", inplace=True)
    # result.index.astype(int)

    result.index.name = None

    tm.assert_frame_equal(result, test_frame1)


def test_roundtrip():
    for arr in basic_arrays + record_arrays:
        arr2 = roundtrip(arr)
        assert_array_equal(arr, arr2)

