
def test_simple():
    rl = rewriterule(Basic(p, S(1)), Basic(p, S(2)), variables=(p,))
    assert list(rl(Basic(S(3), S(1)))) == [Basic(S(3), S(2))]

    p1 = p**2
    p2 = p**3
    rl = rewriterule(p1, p2, variables=(p,))

    expr = x**2
    assert list(rl(expr)) == [x**3]


def test_simple():
    # Gruntz' theses pp. 91 to 96
    # 6.6
    e = sin(1/x + exp(-x)) - sin(1/x)
    assert e.aseries(x) == (1/(24*x**4) - 1/(2*x**2) + 1 + O(x**(-6), (x, oo)))*exp(-x)

    e = exp(x) * (exp(1/x + exp(-x)) - exp(1/x))
    assert e.aseries(x, n=4) == 1/(6*x**3) + 1/(2*x**2) + 1/x + 1 + O(x**(-4), (x, oo))

    e = exp(exp(x) / (1 - 1/x))
    assert e.aseries(x) == exp(exp(x) / (1 - 1/x))

    # The implementation of bound in aseries is incorrect currently. This test
    # should be commented out when that is fixed.
    # assert e.aseries(x, bound=3) == exp(exp(x) / x**2)*exp(exp(x) / x)*exp(-exp(x) + exp(x)/(1 - 1/x) - \
    #         exp(x) / x - exp(x) / x**2) * exp(exp(x))

    e = exp(sin(1/x + exp(-exp(x)))) - exp(sin(1/x))
    assert e.aseries(x, n=4) == (-1/(2*x**3) + 1/x + 1 + O(x**(-4), (x, oo)))*exp(-exp(x))

    e3 = lambda x:exp(exp(exp(x)))
    e = e3(x)/e3(x - 1/e3(x))
    assert e.aseries(x, n=3) == 1 + exp(2*x + 2*exp(x))*exp(-2*exp(exp(x)))/2\
            - exp(2*x + exp(x))*exp(-2*exp(exp(x)))/2 - exp(x + exp(x))*exp(-2*exp(exp(x)))/2\
            + exp(x + exp(x))*exp(-exp(exp(x))) + O(exp(-3*exp(exp(x))), (x, oo))

    e = exp(exp(x)) * (exp(sin(1/x + 1/exp(exp(x)))) - exp(sin(1/x)))
    assert e.aseries(x, n=4) == -1/(2*x**3) + 1/x + 1 + O(x**(-4), (x, oo))

    n = Symbol('n', integer=True)
    e = (sqrt(n)*log(n)**2*exp(sqrt(log(n))*log(log(n))**2*exp(sqrt(log(log(n)))*log(log(log(n)))**3)))/n
    assert e.aseries(n) == \
            exp(exp(sqrt(log(log(n)))*log(log(log(n)))**3)*sqrt(log(n))*log(log(n))**2)*log(n)**2/sqrt(n)


def test_simple():
    assert list(x.lseries()) == [x]
    assert list(S.One.lseries(x)) == [1]
    assert not next((x/(x + y)).lseries(y)).has(Order)


def test_simple():
    a = array([[-0.39-0.71j, 5.14-0.64j, -7.86-2.96j, 3.80+0.92j],
               [5.14-0.64j, 8.86+1.81j, -3.52+0.58j, 5.32-1.59j],
               [-7.86-2.96j, -3.52+0.58j, -2.83-0.03j, -1.54-2.86j],
               [3.80+0.92j, 5.32-1.59j, -1.54-2.86j, -0.56+0.12j]])
    b = array([[5., 10, 1, 18],
               [10., 2, 11, 1],
               [1., 11, 19, 9],
               [18., 1, 9, 0]])
    c = array([[52., 97, 112, 107, 50],
               [97., 114, 89, 98, 13],
               [112., 89, 64, 33, 6],
               [107., 98, 33, 60, 73],
               [50., 13, 6, 73, 77]])

    d = array([[2., 2, -4, 0, 4],
               [2., -2, -2, 10, -8],
               [-4., -2, 6, -8, -4],
               [0., 10, -8, 6, -6],
               [4., -8, -4, -6, 10]])
    e = array([[-1.36+0.00j, 0+0j, 0+0j, 0+0j],
               [1.58-0.90j, -8.87+0j, 0+0j, 0+0j],
               [2.21+0.21j, -1.84+0.03j, -4.63+0j, 0+0j],
               [3.91-1.50j, -1.78-1.18j, 0.11-0.11j, -1.84+0.00j]])
    for x in (b, c, d):
        l, d, p = ldl(x)
        assert_allclose(l.dot(d).dot(l.T), x, atol=spacing(1000.), rtol=0)

        u, d, p = ldl(x, lower=False)
        assert_allclose(u.dot(d).dot(u.T), x, atol=spacing(1000.), rtol=0)

    l, d, p = ldl(a, hermitian=False)
    assert_allclose(l.dot(d).dot(l.T), a, atol=spacing(1000.), rtol=0)

    u, d, p = ldl(a, lower=False, hermitian=False)
    assert_allclose(u.dot(d).dot(u.T), a, atol=spacing(1000.), rtol=0)

    # Use upper part for the computation and use the lower part for comparison
    l, d, p = ldl(e.conj().T, lower=0)
    assert_allclose(tril(l.dot(d).dot(l.conj().T)-e), zeros((4, 4)),
                    atol=spacing(1000.), rtol=0)


def test_simple():
    data = np.ones(5, dtype="int64")
    result = cut(data, 4, labels=False)

    expected = np.array([1, 1, 1, 1, 1])
    tm.assert_numpy_array_equal(result, expected, check_dtype=False)


def test_simple():
    buf = StringIO()
    df = pd.DataFrame([1, 2, 3])
    df.to_markdown(buf=buf)
    result = buf.getvalue()
    assert (
        result == "|    |   0 |\n|---:|----:|\n|  0 |   1 |\n|  1 |   2 |\n|  2 |   3 |"
    )


def test_simple():
    # 16 simple tests
    w = "weight"
    edges = [(0, 0, 1), (0, 0, 1.5), (0, 1, 2), (1, 0, 3)]
    for g1 in [nx.Graph(), nx.DiGraph(), nx.MultiGraph(), nx.MultiDiGraph()]:
        g1.add_weighted_edges_from(edges)
        g2 = g1.subgraph(g1.nodes())
        if g1.is_multigraph():
            em = iso.numerical_multiedge_match("weight", 1)
        else:
            em = iso.numerical_edge_match("weight", 1)
        assert nx.is_isomorphic(g1, g2, edge_match=em)

        for mod1, mod2 in [(False, True), (True, False), (True, True)]:
            # mod1 tests a regular edge
            # mod2 tests a selfloop
            if g2.is_multigraph():
                if mod1:
                    data1 = {0: {"weight": 10}}
                if mod2:
                    data2 = {0: {"weight": 1}, 1: {"weight": 2.5}}
            else:
                if mod1:
                    data1 = {"weight": 10}
                if mod2:
                    data2 = {"weight": 2.5}

            g2 = g1.subgraph(g1.nodes()).copy()
            if mod1:
                if not g1.is_directed():
                    g2._adj[1][0] = data1
                    g2._adj[0][1] = data1
                else:
                    g2._succ[1][0] = data1
                    g2._pred[0][1] = data1
            if mod2:
                if not g1.is_directed():
                    g2._adj[0][0] = data2
                else:
                    g2._succ[0][0] = data2
                    g2._pred[0][0] = data2

            assert not nx.is_isomorphic(g1, g2, edge_match=em)


def test_simple():
    assert 1 + 1 == 2


def test_simple():
    fig = plt.figure()
    pickle.dump(fig, BytesIO(), pickle.HIGHEST_PROTOCOL)

    ax = plt.subplot(121)
    pickle.dump(ax, BytesIO(), pickle.HIGHEST_PROTOCOL)

    ax = plt.axes(projection='polar')
    plt.plot(np.arange(10), label='foobar')
    plt.legend()

    pickle.dump(ax, BytesIO(), pickle.HIGHEST_PROTOCOL)

#    ax = plt.subplot(121, projection='hammer')
#    pickle.dump(ax, BytesIO(), pickle.HIGHEST_PROTOCOL)

    plt.figure()
    plt.bar(x=np.arange(10), height=np.arange(10))
    pickle.dump(plt.gca(), BytesIO(), pickle.HIGHEST_PROTOCOL)

    fig = plt.figure()
    ax = plt.axes()
    plt.plot(np.arange(10))
    ax.set_yscale('log')
    pickle.dump(fig, BytesIO(), pickle.HIGHEST_PROTOCOL)


def test_simple(verbose=None):
    raise_check(f, verbose=verbose)

