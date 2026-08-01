
def test_complement():
    # No args:
    assert complement(lambda: False)()
    assert not complement(lambda: True)()

    # Single arity:
    assert complement(iseven)(1)
    assert not complement(iseven)(2)
    assert complement(complement(iseven))(2)
    assert not complement(complement(isodd))(2)

    # Multiple arities:
    both_even = lambda a, b: iseven(a) and iseven(b)
    assert complement(both_even)(1, 2)
    assert not complement(both_even)(2, 2)

    # Generic truthiness:
    assert complement(lambda: "")()
    assert complement(lambda: 0)()
    assert complement(lambda: None)()
    assert complement(lambda: [])()

    assert not complement(lambda: "x")()
    assert not complement(lambda: 1)()
    assert not complement(lambda: [1])()


def test_complement():
    f = complement(bool)
    assert f(True) is False
    assert f(False) is True
    g = pickle.loads(pickle.dumps(f))
    assert f(True) == g(True)
    assert f(False) == g(False)


def test_complement():
    assert Complement({1, 2}, {1}) == {2}
    assert Interval(0, 1).complement(S.Reals) == \
        Union(Interval(-oo, 0, True, True), Interval(1, oo, True, True))
    assert Interval(0, 1, True, False).complement(S.Reals) == \
        Union(Interval(-oo, 0, True, False), Interval(1, oo, True, True))
    assert Interval(0, 1, False, True).complement(S.Reals) == \
        Union(Interval(-oo, 0, True, True), Interval(1, oo, False, True))
    assert Interval(0, 1, True, True).complement(S.Reals) == \
        Union(Interval(-oo, 0, True, False), Interval(1, oo, False, True))

    assert S.UniversalSet.complement(S.EmptySet) == S.EmptySet
    assert S.UniversalSet.complement(S.Reals) == S.EmptySet
    assert S.UniversalSet.complement(S.UniversalSet) == S.EmptySet

    assert S.EmptySet.complement(S.Reals) == S.Reals

    assert Union(Interval(0, 1), Interval(2, 3)).complement(S.Reals) == \
        Union(Interval(-oo, 0, True, True), Interval(1, 2, True, True),
              Interval(3, oo, True, True))

    assert FiniteSet(0).complement(S.Reals) ==  \
        Union(Interval(-oo, 0, True, True), Interval(0, oo, True, True))

    assert (FiniteSet(5) + Interval(S.NegativeInfinity,
                                    0)).complement(S.Reals) == \
        Interval(0, 5, True, True) + Interval(5, S.Infinity, True, True)

    assert FiniteSet(1, 2, 3).complement(S.Reals) == \
        Interval(S.NegativeInfinity, 1, True, True) + \
        Interval(1, 2, True, True) + Interval(2, 3, True, True) +\
        Interval(3, S.Infinity, True, True)

    assert FiniteSet(x).complement(S.Reals) == Complement(S.Reals, FiniteSet(x))

    assert FiniteSet(0, x).complement(S.Reals) == Complement(Interval(-oo, 0, True, True) +
                                                             Interval(0, oo, True, True)
                                                             , FiniteSet(x), evaluate=False)

    square = Interval(0, 1) * Interval(0, 1)
    notsquare = square.complement(S.Reals*S.Reals)

    assert all(pt in square for pt in [(0, 0), (.5, .5), (1, 0), (1, 1)])
    assert not any(
        pt in notsquare for pt in [(0, 0), (.5, .5), (1, 0), (1, 1)])
    assert not any(pt in square for pt in [(-1, 0), (1.5, .5), (10, 10)])
    assert all(pt in notsquare for pt in [(-1, 0), (1.5, .5), (10, 10)])


def test_complement():
    null = nx.null_graph()
    empty1 = nx.empty_graph(1)
    empty10 = nx.empty_graph(10)
    K3 = nx.complete_graph(3)
    K5 = nx.complete_graph(5)
    K10 = nx.complete_graph(10)
    P2 = nx.path_graph(2)
    P3 = nx.path_graph(3)
    P5 = nx.path_graph(5)
    P10 = nx.path_graph(10)
    # complement of the complete graph is empty

    G = nx.complement(K3)
    assert nx.is_isomorphic(G, nx.empty_graph(3))
    G = nx.complement(K5)
    assert nx.is_isomorphic(G, nx.empty_graph(5))
    # for any G, G=complement(complement(G))
    P3cc = nx.complement(nx.complement(P3))
    assert nx.is_isomorphic(P3, P3cc)
    nullcc = nx.complement(nx.complement(null))
    assert nx.is_isomorphic(null, nullcc)
    b = nx.bull_graph()
    bcc = nx.complement(nx.complement(b))
    assert nx.is_isomorphic(b, bcc)

