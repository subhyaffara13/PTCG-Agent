
def test_empty(tmp_path, config):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(config, encoding="utf-8")

    # Make sure no error is raised
    assert read_configuration(pyproject) == {}


def test_empty(hypotest, args, kwds, n_samples, n_outputs, paired, unpacker):
    # test for correct output shape when at least one input is empty
    if hypotest in {stats.kruskal, stats.friedmanchisquare} and not SCIPY_XSLOW:
        pytest.skip("Too slow.")

    if hypotest in override_propagate_funcs:
        reason = "Doesn't follow the usual pattern. Tested separately."
        pytest.skip(reason=reason)

    if unpacker is None:
        unpacker = lambda res: (res[0], res[1])  # noqa: E731

    def small_data_generator(n_samples, n_dims):

        def small_sample_generator(n_dims):
            # return all possible "small" arrays in up to n_dim dimensions
            for i in n_dims:
                # "small" means with size along dimension either 0 or 1
                for combo in combinations_with_replacement([0, 1, 2], i):
                    yield np.zeros(combo)

        # yield all possible combinations of small samples
        gens = [small_sample_generator(n_dims) for i in range(n_samples)]
        yield from product(*gens)

    n_dims = [1, 2, 3]
    for samples in small_data_generator(n_samples, n_dims):

        # this test is only for arrays of zero size
        if not any(sample.size == 0 for sample in samples):
            continue

        max_axis = max(sample.ndim for sample in samples)

        # need to test for all valid values of `axis` parameter, too
        for axis in range(-max_axis, max_axis):

            try:
                # After broadcasting, all arrays are the same shape, so
                # the shape of the output should be the same as a single-
                # sample statistic. Use np.mean as a reference.
                concat = stats._axis_nan_policy._broadcast_concatenate(samples, axis,
                                                                       paired=paired)
                with warnings.catch_warnings():
                    warnings.filterwarnings(
                        "ignore", "Mean of empty slice", RuntimeWarning)
                    warnings.filterwarnings(
                        "ignore", "invalid value encountered", RuntimeWarning)
                    expected = np.mean(concat, axis=axis) * np.nan
                    mask = np.isnan(expected)
                    expected = [np.asarray(expected.copy()) for i in range(n_outputs)]

                if hypotest in empty_special_case_funcs:
                    empty_val = hypotest(*([[]]*len(samples)), *args, **kwds)
                    empty_val = list(unpacker(empty_val))
                    for i in range(n_outputs):
                        expected[i][mask] = empty_val[i]

                if expected[0].size and hypotest not in too_small_special_case_funcs:
                    message = (too_small_1d_not_omit if max_axis == 1
                               else too_small_nd_not_omit)
                    with pytest.warns(SmallSampleWarning, match=message):
                        res = hypotest(*samples, *args, axis=axis, **kwds)
                else:
                    with warnings.catch_warnings():
                        # f_oneway special case
                        msg = "all input arrays have length 1"
                        warnings.filterwarnings("ignore", msg, SmallSampleWarning)
                        res = hypotest(*samples, *args, axis=axis, **kwds)
                res = unpacker(res)

                for i in range(n_outputs):
                    assert_equal(res[i], expected[i])

            except ValueError:
                # confirm that the arrays truly are not broadcastable
                assert not _check_arrays_broadcastable(samples,
                                                       None if paired else axis)

                # confirm that _both_ `_broadcast_concatenate` and `hypotest`
                # produce this information.
                message = "Array shapes are incompatible for broadcasting."
                with pytest.raises(ValueError, match=message):
                    stats._axis_nan_policy._broadcast_concatenate(samples, axis, paired)
                with pytest.raises(ValueError, match=message):
                    hypotest(*samples, *args, axis=axis, **kwds)


def test_empty():
    x = np.array([1, 2, 3])
    c = CanonicalConstraint.empty(3)
    assert_equal(c.n_eq, 0)
    assert_equal(c.n_ineq, 0)

    c_eq, c_ineq = c.fun(x)
    assert_array_equal(c_eq, [])
    assert_array_equal(c_ineq, [])

    J_eq, J_ineq = c.jac(x)
    assert_array_equal(J_eq, np.empty((0, 3)))
    assert_array_equal(J_ineq, np.empty((0, 3)))

    H = c.hess(x, None, None).toarray()
    assert_array_equal(H, np.zeros((3, 3)))


def test_empty(dt, shape, side):
    a = np.empty(shape, dtype=dt)
    m, n = shape
    p_shape = (m, m) if side == 'left' else (n, n)

    u, p = polar(a, side=side)
    u_n, p_n = polar(np.eye(5, dtype=dt))

    assert_equal(u.dtype, u_n.dtype)
    assert_equal(p.dtype, p_n.dtype)
    assert u.shape == shape
    assert p.shape == p_shape
    assert np.all(p == 0)


def test_empty(dt_c, dt_b):
    c = np.array([], dtype=dt_c)
    b = np.array([], dtype=dt_b)
    x = solve_toeplitz(c, b)
    assert x.shape == (0,)
    assert x.dtype == solve_toeplitz(np.array([2, 1], dtype=dt_c),
                                      np.ones(2, dtype=dt_b)).dtype

    b = np.empty((0, 0), dtype=dt_b)
    x1 = solve_toeplitz(c, b)
    assert x1.shape == (0, 0)
    assert x1.dtype == x.dtype


def test_empty():
    def fun(t, y):
        return np.zeros((0,))

    y0 = np.zeros((0,))

    for method in ['RK23', 'RK45', 'DOP853', 'Radau', 'BDF', 'LSODA']:
        sol = assert_no_warnings(solve_ivp, fun, [0, 10], y0,
                                 method=method, dense_output=True)
        assert_equal(sol.sol(10), np.zeros((0,)))
        assert_equal(sol.sol([1, 2, 3]), np.zeros((0, 3)))

    for method in ['RK23', 'RK45', 'DOP853', 'Radau', 'BDF', 'LSODA']:
        sol = assert_no_warnings(solve_ivp, fun, [0, np.inf], y0,
                                 method=method, dense_output=True)
        assert_equal(sol.sol(10), np.zeros((0,)))
        assert_equal(sol.sol([1, 2, 3]), np.zeros((0, 3)))


def test_empty(frame_or_series, all_boolean_reductions):
    # GH 45231
    kwargs = {"columns": ["a"]} if frame_or_series is DataFrame else {"name": "a"}
    obj = frame_or_series(**kwargs, dtype=object)
    result = getattr(obj.groupby(obj.index), all_boolean_reductions)()
    expected = frame_or_series(**kwargs, dtype=bool)
    tm.assert_equal(result, expected)


def test_empty(keys):
    # GH 26411
    df = DataFrame([], columns=["a", "b"], index=TimedeltaIndex([]))
    result = df.groupby(keys).resample(rule=pd.to_timedelta("00:00:01")).mean()
    expected_columns = ["b"] if keys == ["a"] else []
    expected = (
        DataFrame(columns=["a", "b"])
        .set_index(keys, drop=False)
        .set_index(TimedeltaIndex([]), append=True)[expected_columns]
    )
    if len(keys) == 1:
        expected.index.name = keys[0]

    tm.assert_frame_equal(result, expected)


def test_empty(input_kwargs, result_kwargs):
    # see gh-16302
    ser = Series([], dtype=object)
    result = to_numeric(ser, **input_kwargs)

    expected = Series([], **result_kwargs)
    tm.assert_series_equal(result, expected)


def test_empty():
    s = pd.Series(dtype=object)
    result = s.explode()
    expected = s.copy()
    tm.assert_series_equal(result, expected)


def test_empty(idx):
    # GH 15270
    assert not idx.empty
    assert idx[:0].empty


def test_empty():
    x = numpy.matlib.empty((2,))
    assert_(isinstance(x, np.matrix))
    assert_(x.shape, (1, 2))


def test_empty():
    with pytest.raises(nx.NetworkXException):
        G = nx.empty_graph()
        nx.second_order_centrality(G)


def test_empty():
    G = nx.empty_graph(5)
    assert average_clustering(G, trials=len(G) // 2) == 0


def test_empty(fig_test, fig_ref):
    mpl.rcParams['text.usetex'] = True
    fig_test.text(.5, .5, "% a comment")

