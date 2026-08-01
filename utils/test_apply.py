
def test_apply():
    assert apply(double, 5) == 10
    assert tuple(map(apply, [double, inc, double], [10, 500, 8000])) == (20, 501, 16000)
    assert raises(TypeError, apply)


def test_apply(xp):
    atol = 1e-12
    # Broadcast shape: (6, 5, 4, 2) ( + (3,) for vectors, + (4,) for rotations)
    vector_shapes = [(), (1,), (2,), (1, 2), (5, 1, 2)]
    tf_shapes = [(), (1,), (2,), (1, 2), (4, 2), (1, 4, 2), (5, 4, 2), (6, 5, 4, 2)]
    rng = np.random.default_rng(123)

    for tf_shape, v_shape in product(tf_shapes, vector_shapes):
        # Random rotation and translation
        t = xp.asarray(rng.normal(size=tf_shape + (3,)))
        q = xp.asarray(rng.normal(size=tf_shape + (4,)))
        r = Rotation.from_quat(q)
        tf = RigidTransform.from_components(t, r)

        vecs = xp.asarray(rng.normal(size=v_shape + (3,)))
        expected = t + r.apply(vecs)
        res = tf.apply(vecs)
        assert res.shape == np.broadcast_shapes(tf_shape, v_shape) + (3,)
        xp_assert_close(res, expected, atol=atol)


def test_apply(float_frame, engine, request):
    if engine == "numba":
        mark = pytest.mark.xfail(reason="numba engine not supporting numpy ufunc yet")
        request.node.add_marker(mark)
    with np.errstate(all="ignore"):
        # ufunc
        result = np.sqrt(float_frame["A"])
        expected = float_frame.apply(np.sqrt, engine=engine)["A"]
        tm.assert_series_equal(result, expected)

        # aggregator
        result = float_frame.apply(np.mean, engine=engine)["A"]
        expected = np.mean(float_frame["A"])
        assert result == expected

        d = float_frame.index[0]
        result = float_frame.apply(np.mean, axis=1, engine=engine)
        expected = np.mean(float_frame.xs(d))
        assert result[d] == expected
        assert result.index is float_frame.index


def test_apply(datetime_series, by_row):
    result = datetime_series.apply(np.sqrt, by_row=by_row)
    with np.errstate(all="ignore"):
        expected = np.sqrt(datetime_series)
    tm.assert_series_equal(result, expected)

    # element-wise apply (ufunc)
    result = datetime_series.apply(np.exp, by_row=by_row)
    expected = np.exp(datetime_series)
    tm.assert_series_equal(result, expected)

    # empty series
    s = Series(dtype=object, name="foo", index=Index([], name="bar"))
    rs = s.apply(lambda x: x, by_row=by_row)
    tm.assert_series_equal(s, rs)

    # check all metadata (GH 9322)
    assert s is not rs
    assert s.index is rs.index
    assert s.dtype == rs.dtype
    assert s.name == rs.name

    # index but no data
    s = Series(index=[1, 2, 3], dtype=np.float64)
    rs = s.apply(lambda x: x, by_row=by_row)
    tm.assert_series_equal(s, rs)


def test_apply(ordered):
    # GH 10138

    dense = Categorical(list("abc"), ordered=ordered)

    # 'b' is in the categories but not in the list
    missing = Categorical(list("aaa"), categories=["a", "b"], ordered=ordered)
    values = np.arange(len(dense))
    df = DataFrame({"missing": missing, "dense": dense, "values": values})
    grouped = df.groupby(["missing", "dense"], observed=True)

    # missing category 'b' should still exist in the output index
    idx = MultiIndex.from_arrays([missing, dense], names=["missing", "dense"])
    expected = DataFrame([0, 1, 2.0], index=idx, columns=["values"])

    result = grouped.apply(lambda x: np.mean(x, axis=0))
    tm.assert_frame_equal(result, expected)

    result = grouped.mean()
    tm.assert_frame_equal(result, expected)

    result = grouped.agg(np.mean)
    tm.assert_frame_equal(result, expected)

    # but for transform we should still get back the original index
    idx = MultiIndex.from_arrays([missing, dense], names=["missing", "dense"])
    expected = Series(1, index=idx)
    result = grouped.apply(lambda x: 1)
    tm.assert_series_equal(result, expected)


def test_apply(test_frame):
    g = test_frame.groupby("A")
    r = g.resample("2s")

    # reduction
    expected = g.resample("2s").sum()

    def f_0(x):
        return x.resample("2s").sum()

    result = r.apply(f_0)
    tm.assert_frame_equal(result, expected)

    def f_1(x):
        return x.resample("2s").apply(lambda y: y.sum())

    result = g.apply(f_1)
    tm.assert_frame_equal(result, expected)


def test_apply(test_series):
    grouper = Grouper(freq="YE", label="right", closed="right")

    grouped = test_series.groupby(grouper)

    def f(x):
        return x.sort_values()[-3:]

    applied = grouped.apply(f)
    expected = test_series.groupby(lambda x: x.year).apply(f)

    applied.index = applied.index.droplevel(0)
    expected.index = expected.index.droplevel(0)
    tm.assert_series_equal(applied, expected)

