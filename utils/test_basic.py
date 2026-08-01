
def test_basic():
    assert list(unify(a, x, {})) == [{x: a}]
    assert list(unify(a, x, {x: 10})) == []
    assert list(unify(1, x, {})) == [{x: 1}]
    assert list(unify(a, a, {})) == [{}]
    assert list(unify((w, x), (y, z), {})) == [{w: y, x: z}]
    assert list(unify(x, (a, b), {})) == [{x: (a, b)}]

    assert list(unify((a, b), (x, x), {})) == []
    assert list(unify((y, z), (x, x), {}))!= []
    assert list(unify((a, (b, c)), (a, (x, y)), {})) == [{x: b, y: c}]


def test_basic():
    assert lambdarepr(x*y) == "x*y"
    assert lambdarepr(x + y) in ["y + x", "x + y"]
    assert lambdarepr(x**y) == "x**y"


def test_basic():
    assert qapply(Jz*po) == hbar*po
    assert qapply(Jx*z) == hbar*po/sqrt(2) + hbar*mo/sqrt(2)
    assert qapply((Jplus + Jminus)*z/sqrt(2)) == hbar*po + hbar*mo
    assert qapply(Jz*(po + mo)) == hbar*po - hbar*mo
    assert qapply(Jz*po + Jz*mo) == hbar*po - hbar*mo
    assert qapply(Jminus*Jminus*po) == 2*hbar**2*mo
    assert qapply(Jplus**2*mo) == 2*hbar**2*po
    assert qapply(Jplus**2*Jminus**2*po) == 4*hbar**4*po


def test_basic():
    def j(a, b):
        x = a
        x = +a
        x = -a
        x = a + b
        x = a - b
        x = a*b
        x = a/b
        x = a**b
        del x
    assert dotest(j)


def test_basic():
    def s(a, b):
        x = a
        x = +a
        x = -a
        x = a + b
        x = a - b
        x = a*b
        x = a/b
        x = a**b
        del x
    assert dotest(s)


def test_basic():

    message = "`mpmath.mp.dps <= 15`. Set a higher precision..."
    with pytest.raises(RuntimeError, match=message):
        rd.Normal()

    mpmath.dps = 20
    message = "`mpmath.dps` has been assigned. This is not intended usage..."
    with pytest.raises(RuntimeError, match=message):
        rd.Normal()
    del mpmath.dps

    mp.dps = 20  # high enough to pass, not unreasonably slow

    # Basic tests of the mpmath distribution infrastructure using a SciPy
    # distribution as a reference. The intent is just to make sure that the
    # implementations do not have *mistakes* and that broadcasting is working
    # as expected. The accuracy is what it is.

    rng = np.random.default_rng(6716188855217730280)

    x = rng.random(size=3)
    a = rng.random(size=(2, 1))
    rtol = 1e-15

    dist = rd.SkewNormal(a=a)
    dist_ref = stats.skewnorm(a)

    assert_allclose(dist.pdf(x), dist_ref.pdf(x), rtol=rtol)
    assert_allclose(dist.cdf(x), dist_ref.cdf(x), rtol=rtol)
    assert_allclose(dist.sf(x), dist_ref.sf(x), rtol=rtol)
    assert_allclose(dist.ppf(x), dist_ref.ppf(x), rtol=rtol)
    assert_allclose(dist.isf(x), dist_ref.isf(x), rtol=rtol)
    assert_allclose(dist.logpdf(x), dist_ref.logpdf(x), rtol=rtol)
    assert_allclose(dist.logcdf(x), dist_ref.logcdf(x), rtol=rtol)
    assert_allclose(dist.logsf(x), dist_ref.logsf(x), rtol=rtol)
    assert_allclose(dist.support(), dist_ref.support(), rtol=rtol)
    assert_allclose(dist.entropy(), dist_ref.entropy(), rtol=rtol)
    assert_allclose(dist.mean(), dist_ref.mean(), rtol=rtol)
    assert_allclose(dist.var(), dist_ref.var(), rtol=rtol)
    assert_allclose(dist.skew(), dist_ref.stats('s'), rtol=rtol)
    assert_allclose(dist.kurtosis(), dist_ref.stats('k'), rtol=rtol)


def test_basic():
    # test that 'method' arg is really optional
    res = least_squares(fun_trivial, 2.0)
    assert_allclose(res.x, 0, atol=1e-10)


def test_basic():
    cats = Categorical(
        ["a", "a", "a", "b", "b", "b", "c", "c", "c"],
        categories=["a", "b", "c", "d"],
        ordered=True,
    )
    data = DataFrame({"a": [1, 1, 1, 2, 2, 2, 3, 4, 5], "b": cats})

    exp_index = CategoricalIndex(list("abcd"), name="b", ordered=True)
    expected = DataFrame({"a": [1, 2, 4, np.nan]}, index=exp_index)
    result = data.groupby("b", observed=False).mean()
    tm.assert_frame_equal(result, expected)


def test_basic():
    s = pd.Series([[0, 1, 2], np.nan, [], (3, 4)], index=list("abcd"), name="foo")
    result = s.explode()
    expected = pd.Series(
        [0, 1, 2, np.nan, np.nan, 3, 4], index=list("aaabcdd"), dtype=object, name="foo"
    )
    tm.assert_series_equal(result, expected)


def test_basic(all_parsers):
    parser = all_parsers

    data = "a,a,b,b,b\n1,2,3,4,5"
    result = parser.read_csv(StringIO(data), sep=",")

    expected = DataFrame([[1, 2, 3, 4, 5]], columns=["a", "a.1", "b", "b.1", "b.2"])
    tm.assert_frame_equal(result, expected)


def test_basic():
    data = """\
A         B            C            D
201158    360.242940   149.910199   11950.7
201159    444.953632   166.985655   11788.4
201160    364.136849   183.628767   11806.2
201161    413.836124   184.375703   11916.8
201162    502.953953   173.237159   12468.3
"""
    result = read_fwf(StringIO(data))
    expected = DataFrame(
        [
            [201158, 360.242940, 149.910199, 11950.7],
            [201159, 444.953632, 166.985655, 11788.4],
            [201160, 364.136849, 183.628767, 11806.2],
            [201161, 413.836124, 184.375703, 11916.8],
            [201162, 502.953953, 173.237159, 12468.3],
        ],
        columns=["A", "B", "C", "D"],
    )
    tm.assert_frame_equal(result, expected)


def test_basic(education_df, request):
    # gh43564
    request.applymarker(
        pytest.mark.xfail(
            reason=(
                "pandas default unstable sorting of duplicates"
                "issue with numpy>=1.25 with AVX instructions"
            ),
            strict=False,
        )
    )
    result = education_df.groupby("country")[["gender", "education"]].value_counts(
        normalize=True
    )
    expected = Series(
        data=[0.5, 0.25, 0.25, 0.5, 0.5],
        index=MultiIndex.from_tuples(
            [
                ("FR", "male", "low"),
                ("FR", "male", "medium"),
                ("FR", "female", "high"),
                ("US", "male", "low"),
                ("US", "female", "high"),
            ],
            names=["country", "gender", "education"],
        ),
        name="proportion",
    )
    tm.assert_series_equal(result, expected)


def test_basic(scalar):
    df = pd.DataFrame(
        {scalar: pd.Series([[0, 1, 2], np.nan, [], (3, 4)], index=list("abcd")), "B": 1}
    )
    result = df.explode(scalar)
    expected = pd.DataFrame(
        {
            scalar: pd.Series(
                [0, 1, 2, np.nan, np.nan, 3, 4], index=list("aaabcdd"), dtype=object
            ),
            "B": 1,
        }
    )
    tm.assert_frame_equal(result, expected)


def test_basic():
    """Joining multiple subtrees at a root node."""
    trees = [(nx.full_rary_tree(2, 2**2 - 1), 0) for i in range(2)]
    expected = nx.full_rary_tree(2, 2**3 - 1)
    actual = nx.join_trees(trees, label_attribute="old_labels")
    assert nx.is_isomorphic(actual, expected)
    assert _check_custom_label_attribute(trees, actual, "old_labels")

    actual_without_label = nx.join_trees(trees)
    assert nx.is_isomorphic(actual_without_label, expected)
    # check that no labels were stored
    assert all(not data for _, data in actual_without_label.nodes(data=True))


def test_basic():
    a = [0, 1, 2]
    pa = pickle.dumps(a)
    pmath = pickle.dumps(math) #XXX: FAILS in pickle
    pmap = pickle.dumps(map)
    # ...
    la = pickle.loads(pa)
    lmath = pickle.loads(pmath)
    lmap = pickle.loads(pmap)
    assert list(map(math.sin, a)) == list(lmap(lmath.sin, la))

