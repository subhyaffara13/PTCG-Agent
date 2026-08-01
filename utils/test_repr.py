
def test_repr():
    assert "pybind11_type" in repr(type(UserType))
    assert "UserType" in repr(UserType)


def test_repr():
    T = Poly(x**2 + 7)
    ZK, dK = round_two(T)
    P = prime_decomp(2, T, dK=dK, ZK=ZK)
    assert repr(P[0]) == '[ (2, (3*x + 1)/2) e=1, f=1 ]'
    assert P[0].repr(field_gen=theta) == '[ (2, (3*theta + 1)/2) e=1, f=1 ]'
    assert P[0].repr(field_gen=theta, just_gens=True) == '(2, (3*theta + 1)/2)'


def test_repr():
    assert eval(repr(kilo)) == kilo
    assert eval(repr(kibi)) == kibi


def test_repr():
    assert repr(Circle((0, 1), 2)) == 'Circle(Point2D(0, 1), 2)'


def test_repr(func):
    assert func.__name__ in repr(func)
    assert "locals" not in repr(func)


def test_repr(xp):
    actual = repr(RigidTransform.from_matrix(xp.eye(4)))
    expected = """\
RigidTransform.from_matrix(array([[1., 0., 0., 0.],
                                  [0., 1., 0., 0.],
                                  [0., 0., 1., 0.],
                                  [0., 0., 0., 1.]]))"""
    if is_numpy(xp):
        assert actual == expected
    else:
        assert actual.startswith("RigidTransform.from_matrix(")

    tf = RigidTransform.from_matrix(xp.asarray(RigidTransform.identity(2).as_matrix()))
    actual = repr(tf)
    expected = """\
RigidTransform.from_matrix(array([[[1., 0., 0., 0.],
                                   [0., 1., 0., 0.],
                                   [0., 0., 1., 0.],
                                   [0., 0., 0., 1.]],
                           
                                  [[1., 0., 0., 0.],
                                   [0., 1., 0., 0.],
                                   [0., 0., 1., 0.],
                                   [0., 0., 0., 1.]]]))"""
    if is_numpy(xp):
        assert actual == expected
    else:
        assert actual.startswith("RigidTransform.from_matrix(")


def test_repr(xp):
    A = interface.LinearOperator(shape=(1, 1), matvec=lambda x: xp.asarray([1]), xp=xp)
    repr_A = repr(A)
    assert 'unspecified dtype' not in repr_A, repr_A


def test_repr():
    # GH18203
    result = repr(Grouper(key="A", level="B"))
    expected = "Grouper(key='A', level='B', sort=False, dropna=True)"
    assert result == expected


def test_repr():
    # GH18203
    result = repr(Grouper(key="A", freq="h"))
    expected = (
        "TimeGrouper(key='A', freq=<Hour>, sort=True, dropna=True, "
        "closed='left', label='left', how='mean', "
        "convention='e', origin='start_day')"
    )
    assert result == expected

    result = repr(Grouper(key="A", freq="h", origin="2000-01-01"))
    expected = (
        "TimeGrouper(key='A', freq=<Hour>, sort=True, dropna=True, "
        "closed='left', label='left', how='mean', "
        "convention='e', origin=Timestamp('2000-01-01 00:00:00'))"
    )
    assert result == expected


def test_repr():
    assert repr(NA) == "<NA>"
    assert str(NA) == "<NA>"


def test_repr(td, expected_repr):
    assert repr(td) == expected_repr


def test_repr(temp_hdfstore, performance_warning, using_infer_string):
    store = temp_hdfstore
    repr(store)
    store.info()
    store["a"] = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )
    store["b"] = Series(range(10), dtype="float64", index=[f"i_{i}" for i in range(10)])
    store["c"] = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )

    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    df["obj1"] = "foo"
    df["obj2"] = "bar"
    df["bool1"] = df["A"] > 0
    df["bool2"] = df["B"] > 0
    df["bool3"] = True
    df["int1"] = 1
    df["int2"] = 2
    df["timestamp1"] = Timestamp("20010102")
    df["timestamp2"] = Timestamp("20010103")
    df["datetime1"] = dt.datetime(2001, 1, 2, 0, 0)
    df["datetime2"] = dt.datetime(2001, 1, 3, 0, 0)
    df.loc[df.index[3:6], ["obj1"]] = np.nan
    df = df._consolidate()

    warning = None if using_infer_string else performance_warning
    msg = "cannot\nmap directly to c-types .* dtype='object'"
    with tm.assert_produces_warning(warning, match=msg):
        store["df"] = df

    # make a random group in hdf space
    store._handle.create_group(store._handle.root, "bah")

    assert store.filename in repr(store)
    assert store.filename in str(store)
    store.info()


def test_repr():
    df = pd.DataFrame({"A": pd.array([True, False, None], dtype="boolean")})
    expected = "       A\n0   True\n1  False\n2   <NA>"
    assert repr(df) == expected

    expected = "0     True\n1    False\n2     <NA>\nName: A, dtype: boolean"
    assert repr(df.A) == expected

    expected = "<BooleanArray>\n[True, False, <NA>]\nLength: 3, dtype: boolean"
    assert repr(df.A.array) == expected


def test_repr():
    # GH#25022
    arr = IntervalArray.from_tuples([(0, 1), (1, 2)])
    result = repr(arr)
    expected = (
        "<IntervalArray>\n[(0, 1], (1, 2]]\nLength: 2, dtype: interval[int64, right]"
    )
    assert result == expected


def test_repr():
    dtype = NumpyEADtype(np.dtype("int64"))
    assert repr(dtype) == "NumpyEADtype('int64')"


def test_repr():
    # GH-34352
    result = str(SparseDtype("int64", fill_value=0))
    expected = "Sparse[int64, 0]"
    assert result == expected

    result = str(SparseDtype(object, fill_value="0"))
    expected = "Sparse[object, '0']"
    assert result == expected


def test_repr(dtype):
    df = pd.DataFrame({"A": pd.array(["a", pd.NA, "b"], dtype=dtype)})
    if dtype.na_value is np.nan:
        expected = "     A\n0    a\n1  NaN\n2    b"
    else:
        expected = "      A\n0     a\n1  <NA>\n2     b"
    assert repr(df) == expected

    if dtype.na_value is np.nan:
        expected = "0      a\n1    NaN\n2      b\nName: A, dtype: str"
    else:
        expected = "0       a\n1    <NA>\n2       b\nName: A, dtype: string"
    assert repr(df.A) == expected

    if dtype.storage == "pyarrow" and dtype.na_value is pd.NA:
        arr_name = "ArrowStringArray"
        expected = f"<{arr_name}>\n['a', <NA>, 'b']\nLength: 3, dtype: string"
    elif dtype.storage == "pyarrow" and dtype.na_value is np.nan:
        arr_name = "ArrowStringArray"
        expected = f"<{arr_name}>\n['a', nan, 'b']\nLength: 3, dtype: str"
    elif dtype.storage == "python" and dtype.na_value is np.nan:
        arr_name = "StringArray"
        expected = f"<{arr_name}>\n['a', nan, 'b']\nLength: 3, dtype: str"
    else:
        arr_name = "StringArray"
        expected = f"<{arr_name}>\n['a', <NA>, 'b']\nLength: 3, dtype: string"
    assert repr(df.A.array) == expected


def test_repr():
    fig, ax = plt.subplots()
    ax.set_label('label')
    ax.set_title('title')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    assert repr(ax) == (
        "<Axes: "
        "label='label', title={'center': 'title'}, xlabel='x', ylabel='y'>")


def test_repr():
    ss = gridspec.GridSpec(3, 3)[2, 1:3]
    assert repr(ss) == "GridSpec(3, 3)[2:3, 1:3]"

    ss = gridspec.GridSpec(2, 2,
                           height_ratios=(3, 1),
                           width_ratios=(1, 3))
    assert repr(ss) == \
        "GridSpec(2, 2, height_ratios=(3, 1), width_ratios=(1, 3))"

