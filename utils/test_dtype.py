
def test_dtype(simple_dtype):
    from sys import byteorder

    e = "<" if byteorder == "little" else ">"

    assert [x.replace(" ", "") for x in m.print_dtypes()] == [
        simple_dtype_fmt(),
        packed_dtype_fmt(),
        f"[('a',{simple_dtype_fmt()}),('b',{packed_dtype_fmt()})]",
        partial_dtype_fmt(),
        partial_nested_fmt(),
        "[('a','S3'),('b','S3')]",
        (
            "{'names':['a','b','c','d'],"
            f"'formats':[('S4',(3,)),('{e}i4',(2,)),('u1',(3,)),('{e}f4',(4,2))],"
            "'offsets':[0,12,20,24],'itemsize':56}"
        ),
        "[('e1','" + e + "i8'),('e2','u1')]",
        "[('x','i1'),('y','" + e + "u8')]",
        "[('cflt','" + e + "c8'),('cdbl','" + e + "c16')]",
    ]

    d1 = np.dtype(
        {
            "names": ["a", "b"],
            "formats": ["int32", "float64"],
            "offsets": [1, 10],
            "itemsize": 20,
        }
    )
    d2 = np.dtype([("a", "i4"), ("b", "f4")])
    assert m.test_dtype_ctors() == [
        np.dtype("int32"),
        np.dtype("float64"),
        np.dtype("bool"),
        d1,
        d1,
        np.dtype("uint32"),
        d2,
        np.dtype("d"),
    ]

    assert m.test_dtype_methods() == [
        np.dtype("int32"),
        simple_dtype,
        False,
        True,
        np.dtype("int32").itemsize,
        simple_dtype.itemsize,
    ]

    assert m.trailing_padding_dtype() == m.buffer_to_dtype(
        np.zeros(1, m.trailing_padding_dtype())
    )

    expected_chars = "bhilqBHILQefdgFDG?MmO"
    assert m.test_dtype_kind() == list("iiiiiuuuuuffffcccbMmO")
    assert m.test_dtype_char_() == list(expected_chars)
    assert m.test_dtype_num() == [np.dtype(ch).num for ch in expected_chars]
    assert m.test_dtype_byteorder() == [np.dtype(ch).byteorder for ch in expected_chars]
    assert m.test_dtype_alignment() == [np.dtype(ch).alignment for ch in expected_chars]
    assert m.test_dtype_flags() == [chr(np.dtype(ch).flags) for ch in expected_chars]


def test_dtype():
    """ Test specifying specific data types through the dtype argument. """
    for dtype in ['float32', 'float64', 'int8', 'int16', 'int32', 'int64']:
        assert aesara_code_(x, dtypes={x: dtype}).type.dtype == dtype

    # "floatX" type
    assert aesara_code_(x, dtypes={x: 'floatX'}).type.dtype in ('float32', 'float64')

    # Type promotion
    assert aesara_code_(x + 1, dtypes={x: 'float32'}).type.dtype == 'float32'
    assert aesara_code_(x + y, dtypes={x: 'float64', y: 'float32'}).type.dtype == 'float64'


def test_dtype():
    """ Test specifying specific data types through the dtype argument. """
    for dtype in ['float32', 'float64', 'int8', 'int16', 'int32', 'int64']:
        assert theano_code_(x, dtypes={x: dtype}).type.dtype == dtype

    # "floatX" type
    assert theano_code_(x, dtypes={x: 'floatX'}).type.dtype in ('float32', 'float64')

    # Type promotion
    assert theano_code_(x + 1, dtypes={x: 'float32'}).type.dtype == 'float32'
    assert theano_code_(x + y, dtypes={x: 'float64', y: 'float32'}).type.dtype == 'float64'


def test_dtype(conn, request):
    if conn == "sqlite_str":
        pytest.skip("sqlite_str has no inspection system")

    conn = request.getfixturevalue(conn)

    from sqlalchemy import (
        TEXT,
        String,
    )
    from sqlalchemy.schema import MetaData

    cols = ["A", "B"]
    data = [(0.8, True), (0.9, None)]
    df = DataFrame(data, columns=cols)
    assert df.to_sql(name="dtype_test", con=conn) == 2
    assert df.to_sql(name="dtype_test2", con=conn, dtype={"B": TEXT}) == 2
    meta = MetaData()
    meta.reflect(bind=conn)
    sqltype = meta.tables["dtype_test2"].columns["B"].type
    assert isinstance(sqltype, TEXT)
    msg = "The type of B is not a SQLAlchemy type"
    with pytest.raises(ValueError, match=msg):
        df.to_sql(name="error", con=conn, dtype={"B": str})

    # GH9083
    assert df.to_sql(name="dtype_test3", con=conn, dtype={"B": String(10)}) == 2
    meta.reflect(bind=conn)
    sqltype = meta.tables["dtype_test3"].columns["B"].type
    assert isinstance(sqltype, String)
    assert sqltype.length == 10

    # single dtype
    assert df.to_sql(name="single_dtype_test", con=conn, dtype=TEXT) == 2
    meta.reflect(bind=conn)
    sqltypea = meta.tables["single_dtype_test"].columns["A"].type
    sqltypeb = meta.tables["single_dtype_test"].columns["B"].type
    assert isinstance(sqltypea, TEXT)
    assert isinstance(sqltypeb, TEXT)


def test_dtype(dtype):
    data = """ a    b    c
1    2    3.2
3    4    5.2
"""
    colspecs = [(0, 5), (5, 10), (10, None)]
    result = read_fwf(StringIO(data), colspecs=colspecs, dtype=dtype)

    expected = DataFrame(
        {"a": [1, 3], "b": [2, 4], "c": [3.2, 5.2]}, columns=["a", "b", "c"]
    )

    for col, dt in dtype.items():
        expected[col] = expected[col].astype(dt)

    tm.assert_frame_equal(result, expected)


def test_dtype():
    try:
        import numpy as np

        dti = np.dtype('int')
        assert np.dtype == dill.copy(np.dtype)
        assert dti == dill.copy(dti)
    except ImportError: pass

