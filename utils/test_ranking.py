
def test_ranking():
    assert Permutation.unrank_lex(5, 10).rank() == 10
    p = Permutation.unrank_lex(15, 225)
    assert p.rank() == 225
    p1 = p.next_lex()
    assert p1.rank() == 226
    assert Permutation.unrank_lex(15, 225).rank() == 225
    assert Permutation.unrank_lex(10, 0).is_Identity
    p = Permutation.unrank_lex(4, 23)
    assert p.rank() == 23
    assert p.array_form == [3, 2, 1, 0]
    assert p.next_lex() is None

    p = Permutation([1, 5, 2, 0, 3, 6, 4])
    q = Permutation([[1, 2, 3, 5, 6], [0, 4]])
    a = [Permutation.unrank_trotterjohnson(4, i).array_form for i in range(5)]
    assert a == [[0, 1, 2, 3], [0, 1, 3, 2], [0, 3, 1, 2], [3, 0, 1,
        2], [3, 0, 2, 1] ]
    assert [Permutation(pa).rank_trotterjohnson() for pa in a] == list(range(5))
    assert Permutation([0, 1, 2, 3]).next_trotterjohnson() == \
        Permutation([0, 1, 3, 2])

    assert q.rank_trotterjohnson() == 2283
    assert p.rank_trotterjohnson() == 3389
    assert Permutation([1, 0]).rank_trotterjohnson() == 1
    a = Permutation(list(range(3)))
    b = a
    l = []
    tj = []
    for i in range(6):
        l.append(a)
        tj.append(b)
        a = a.next_lex()
        b = b.next_trotterjohnson()
    assert a == b is None
    assert {tuple(a) for a in l} == {tuple(a) for a in tj}

    p = Permutation([2, 5, 1, 6, 3, 0, 4])
    q = Permutation([[6], [5], [0, 1, 2, 3, 4]])
    assert p.rank() == 1964
    assert q.rank() == 870
    assert Permutation([]).rank_nonlex() == 0
    prank = p.rank_nonlex()
    assert prank == 1600
    assert Permutation.unrank_nonlex(7, 1600) == p
    qrank = q.rank_nonlex()
    assert qrank == 41
    assert Permutation.unrank_nonlex(7, 41) == Permutation(q.array_form)

    a = [Permutation.unrank_nonlex(4, i).array_form for i in range(24)]
    assert a == [
        [1, 2, 3, 0], [3, 2, 0, 1], [1, 3, 0, 2], [1, 2, 0, 3], [2, 3, 1, 0],
        [2, 0, 3, 1], [3, 0, 1, 2], [2, 0, 1, 3], [1, 3, 2, 0], [3, 0, 2, 1],
        [1, 0, 3, 2], [1, 0, 2, 3], [2, 1, 3, 0], [2, 3, 0, 1], [3, 1, 0, 2],
        [2, 1, 0, 3], [3, 2, 1, 0], [0, 2, 3, 1], [0, 3, 1, 2], [0, 2, 1, 3],
        [3, 1, 2, 0], [0, 3, 2, 1], [0, 1, 3, 2], [0, 1, 2, 3]]

    N = 10
    p1 = Permutation(a[0])
    for i in range(1, N+1):
        p1 = p1*Permutation(a[i])
    p2 = Permutation.rmul_with_af(*[Permutation(h) for h in a[N::-1]])
    assert p1 == p2

    ok = []
    p = Permutation([1, 0])
    for i in range(3):
        ok.append(p.array_form)
        p = p.next_nonlex()
        if p is None:
            ok.append(None)
            break
    assert ok == [[1, 0], [0, 1], None]
    assert Permutation([3, 2, 0, 1]).next_nonlex() == Permutation([1, 3, 0, 2])
    assert [Permutation(pa).rank_nonlex() for pa in a] == list(range(24))

