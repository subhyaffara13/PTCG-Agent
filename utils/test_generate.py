
def test_generate():
    from sympy.ntheory.generate import sieve
    sieve._reset()
    assert nextprime(-4) == 2
    assert nextprime(2) == 3
    assert nextprime(5) == 7
    assert nextprime(12) == 13
    assert prevprime(3) == 2
    assert prevprime(7) == 5
    assert prevprime(13) == 11
    assert prevprime(19) == 17
    assert prevprime(20) == 19

    sieve.extend_to_no(9)
    assert sieve._list[-1] == 23

    assert sieve._list[-1] < 31
    assert 31 in sieve

    assert nextprime(90) == 97
    assert nextprime(10**40) == (10**40 + 121)
    primelist = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
                 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
                 79, 83, 89, 97, 101, 103, 107, 109, 113,
                 127, 131, 137, 139, 149, 151, 157, 163,
                 167, 173, 179, 181, 191, 193, 197, 199,
                 211, 223, 227, 229, 233, 239, 241, 251,
                 257, 263, 269, 271, 277, 281, 283, 293]
    for i in range(len(primelist) - 2):
        for j in range(2, len(primelist) - i):
            assert nextprime(primelist[i], j) == primelist[i + j]
            if 3 < i:
                assert nextprime(primelist[i] - 1, j) == primelist[i + j - 1]
    raises(ValueError, lambda: nextprime(2, 0))
    raises(ValueError, lambda: nextprime(2, -1))
    assert prevprime(97) == 89
    assert prevprime(10**40) == (10**40 - 17)

    raises(ValueError, lambda: Sieve(0))
    raises(ValueError, lambda: Sieve(-1))
    for sieve_interval in [1, 10, 11, 1_000_000]:
        s = Sieve(sieve_interval=sieve_interval)
        for head in range(s._list[-1] + 1, (s._list[-1] + 1)**2, 2):
            for tail in range(head + 1, (s._list[-1] + 1)**2):
                A = list(s._primerange(head, tail))
                B = primelist[bisect(primelist, head):bisect_left(primelist, tail)]
                assert A == B
        for k in range(s._list[-1], primelist[-1] - 1, 2):
            s = Sieve(sieve_interval=sieve_interval)
            s.extend(k)
            assert list(s._list) == primelist[:bisect(primelist, k)]
            s.extend(primelist[-1])
            assert list(s._list) == primelist

    assert list(sieve.primerange(10, 1)) == []
    assert list(sieve.primerange(5, 9)) == [5, 7]
    sieve._reset(prime=True)
    assert list(sieve.primerange(2, 13)) == [2, 3, 5, 7, 11]
    assert list(sieve.primerange(13)) == [2, 3, 5, 7, 11]
    assert list(sieve.primerange(8)) == [2, 3, 5, 7]
    assert list(sieve.primerange(-2)) == []
    assert list(sieve.primerange(29)) == [2, 3, 5, 7, 11, 13, 17, 19, 23]
    assert list(sieve.primerange(34)) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]

    assert list(sieve.totientrange(5, 15)) == [4, 2, 6, 4, 6, 4, 10, 4, 12, 6]
    sieve._reset(totient=True)
    assert list(sieve.totientrange(3, 13)) == [2, 2, 4, 2, 6, 4, 6, 4, 10, 4]
    assert list(sieve.totientrange(900, 1000)) == [totient(x) for x in range(900, 1000)]
    assert list(sieve.totientrange(0, 1)) == []
    assert list(sieve.totientrange(1, 2)) == [1]

    assert list(sieve.mobiusrange(5, 15)) == [-1, 1, -1, 0, 0, 1, -1, 0, -1, 1]
    sieve._reset(mobius=True)
    assert list(sieve.mobiusrange(3, 13)) == [-1, 0, -1, 1, -1, 0, 0, 1, -1, 0]
    assert list(sieve.mobiusrange(1050, 1100)) == [mobius(x) for x in range(1050, 1100)]
    assert list(sieve.mobiusrange(0, 1)) == []
    assert list(sieve.mobiusrange(1, 2)) == [1]

    assert list(primerange(10, 1)) == []
    assert list(primerange(2, 7)) == [2, 3, 5]
    assert list(primerange(2, 10)) == [2, 3, 5, 7]
    assert list(primerange(1050, 1100)) == [1051, 1061,
        1063, 1069, 1087, 1091, 1093, 1097]
    s = Sieve()
    for i in range(30, 2350, 376):
        for j in range(2, 5096, 1139):
            A = list(s.primerange(i, i + j))
            B = list(primerange(i, i + j))
            assert A == B
    s = Sieve()
    sieve._reset(prime=True)
    sieve.extend(13)
    for i in range(200):
        for j in range(i, 200):
            A = list(s.primerange(i, j))
            B = list(primerange(i, j))
            assert A == B
    sieve.extend(1000)
    for a, b in [(901, 1103), # a < 1000 < b < 1000**2
                 (806, 1002007), # a < 1000 < 1000**2 < b
                 (2000, 30001), # 1000 < a < b < 1000**2
                 (100005, 1010001), # 1000 < a < 1000**2 < b
                 (1003003, 1005000), # 1000**2 < a < b
                 ]:
        assert list(primerange(a, b)) == list(s.primerange(a, b))
    sieve._reset(prime=True)
    sieve.extend(100000)
    assert len(sieve._list) == len(set(sieve._list))
    s = Sieve()
    assert s[10] == 29

    assert nextprime(2, 2) == 5

    raises(ValueError, lambda: totient(0))

    raises(ValueError, lambda: primorial(0))

    assert mr(1, [2]) is False

    func = lambda i: (i**2 + 1) % 51
    assert next(cycle_length(func, 4)) == (6, 3)
    assert list(cycle_length(func, 4, values=True)) == \
        [4, 17, 35, 2, 5, 26, 14, 44, 50, 2, 5, 26, 14]
    assert next(cycle_length(func, 4, nmax=5)) == (5, None)
    assert list(cycle_length(func, 4, nmax=5, values=True)) == \
        [4, 17, 35, 2, 5]
    sieve.extend(3000)
    assert nextprime(2968) == 2969
    assert prevprime(2930) == 2927
    raises(ValueError, lambda: prevprime(1))
    raises(ValueError, lambda: prevprime(-4))


def test_generate():
    a = Permutation([1, 0])
    g = list(PermutationGroup([a]).generate())
    assert g == [Permutation([0, 1]), Permutation([1, 0])]
    assert len(list(PermutationGroup(Permutation((0, 1))).generate())) == 1
    g = PermutationGroup([a]).generate(method='dimino')
    assert list(g) == [Permutation([0, 1]), Permutation([1, 0])]
    a = Permutation([2, 0, 1])
    b = Permutation([2, 1, 0])
    G = PermutationGroup([a, b])
    g = G.generate()
    v1 = [p.array_form for p in list(g)]
    v1.sort()
    assert v1 == [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0,
        1], [2, 1, 0]]
    v2 = list(G.generate(method='dimino', af=True))
    assert v1 == sorted(v2)
    a = Permutation([2, 0, 1, 3, 4, 5])
    b = Permutation([2, 1, 3, 4, 5, 0])
    g = PermutationGroup([a, b]).generate(af=True)
    assert len(list(g)) == 360

