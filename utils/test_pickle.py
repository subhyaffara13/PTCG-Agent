
def test_pickle(method, kwargs):
    Method = getattr(stats.sampling, method)
    rng1 = Method(**kwargs, random_state=123)
    obj = pickle.dumps(rng1)
    rng2 = pickle.loads(obj)
    assert_equal(rng1.rvs(100), rng2.rvs(100))


def test_pickle(func):
    roundtrip = pickle.loads(pickle.dumps(func))
    assert roundtrip is func


def test_pickle(xp):
    import pickle

    protocol_min = 0 if is_numpy(xp) else 2
    for protocol in range(protocol_min, pickle.HIGHEST_PROTOCOL + 1):
        A = interface.LinearOperator((3, 3), matvec_for_pickle, xp=xp)
        s = pickle.dumps(A, protocol=protocol)
        B = pickle.loads(s)

        for k in A.__dict__:
            assert getattr(A, k) == getattr(B, k)


def test_pickle(temp_file):
    a = pd.Series([1, 2]).set_flags(allows_duplicate_labels=False)
    b = tm.round_trip_pickle(a, temp_file)
    tm.assert_series_equal(a, b)

    a = pd.DataFrame({"A": []}).set_flags(allows_duplicate_labels=False)
    b = tm.round_trip_pickle(a, temp_file)
    tm.assert_frame_equal(a, b)


def test_pickle(temp_file):
    # GH#4606
    p = tm.round_trip_pickle(NaT, temp_file)
    assert p is NaT


def test_pickle(dtype, string_list):
    arr = np.array(string_list, dtype=dtype)

    with tempfile.NamedTemporaryFile("wb", delete=False) as f:
        pickle.dump([arr, dtype], f)

    with open(f.name, "rb") as f:
        res = pickle.load(f)

    assert_array_equal(res[0], arr)
    assert res[1] == dtype

    os.remove(f.name)


def test_pickle():
    count = 0
    for name, func in nx.utils.backends._registered_algorithms.items():
        pickled = pickle.dumps(func.__wrapped__)
        assert pickle.loads(pickled) is func.__wrapped__
        try:
            # Some functions can't be pickled, but it's not b/c of _dispatchable
            pickled = pickle.dumps(func)
        except pickle.PicklingError:
            continue
        assert pickle.loads(pickled) is func
        count += 1
    assert count > 0
    assert pickle.loads(pickle.dumps(nx.inverse_line_graph)) is nx.inverse_line_graph


def test_pickle():

    obj = mpf('0.5')
    assert obj == pickler(obj)

    obj = mpc('0.5','0.2')
    assert obj == pickler(obj)

