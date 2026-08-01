
def test_nD_derangements():
    from sympy.utilities.iterables import (partitions, multiset,
        multiset_derangements, multiset_permutations)
    from sympy.functions.combinatorial.numbers import nD

    got = []
    for i in partitions(8, k=4):
        s = []
        it = 0
        for k, v in i.items():
            for i in range(v):
                s.extend([it]*k)
                it += 1
        ms = multiset(s)
        c1 = sum(1 for i in multiset_permutations(s) if
            all(i != j for i, j in zip(i, s)))
        assert c1 == nD(ms) == nD(ms, 0) == nD(ms, 1)
        v = [tuple(i) for i in multiset_derangements(s)]
        c2 = len(v)
        assert c2 == len(set(v))
        assert c1 == c2
        got.append(c1)
    assert got == [1, 4, 6, 12, 24, 24, 61, 126, 315, 780, 297, 772,
        2033, 5430, 14833]

    assert nD('1112233456', brute=True) == nD('1112233456') == 16356
    assert nD('') == nD([]) == nD({}) == 0
    assert nD({1: 0}) == 0
    raises(ValueError, lambda: nD({1: -1}))
    assert nD('112') == 0
    assert nD(i='112') == 0
    assert [nD(n=i) for i in range(6)] == [0, 0, 1, 2, 9, 44]
    assert nD((i for i in range(4))) == nD('0123') == 9
    assert nD(m=(i for i in range(4))) == 3
    assert nD(m={0: 1, 1: 1, 2: 1, 3: 1}) == 3
    assert nD(m=[0, 1, 2, 3]) == 3
    raises(TypeError, lambda: nD(m=0))
    raises(TypeError, lambda: nD(-1))
    assert nD({-1: 1, -2: 1}) == 1
    assert nD(m={0: 3}) == 0
    raises(ValueError, lambda: nD(i='123', n=3))
    raises(ValueError, lambda: nD(i='123', m=(1,2)))
    raises(ValueError, lambda: nD(n=0, m=(1,2)))
    raises(ValueError, lambda: nD({1: -1}))
    raises(ValueError, lambda: nD(m={-1: 1, 2: 1}))
    raises(ValueError, lambda: nD(m={1: -1, 2: 1}))
    raises(ValueError, lambda: nD(m=[-1, 2]))
    raises(TypeError, lambda: nD({1: x}))
    raises(TypeError, lambda: nD(m={1: x}))
    raises(TypeError, lambda: nD(m={x: 1}))

