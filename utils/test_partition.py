
def test_partition():
    assert list(partition(2, [1, 2, 3, 4])) == [(1, 2), (3, 4)]
    assert list(partition(3, range(7))) == [(0, 1, 2), (3, 4, 5)]
    assert list(partition(3, range(4), pad=-1)) == [(0, 1, 2),
                                                    (3, -1, -1)]
    assert list(partition(2, [])) == []


def test_partition():
    partition_nums = [1, 1, 2, 3, 5, 7, 11, 15, 22]
    for n, p in enumerate(partition_nums):
        assert partition(n) == p

    x = Symbol('x')
    y = Symbol('y', real=True)
    m = Symbol('m', integer=True)
    n = Symbol('n', integer=True, negative=True)
    p = Symbol('p', integer=True, nonnegative=True)
    assert partition(m).is_integer
    assert not partition(m).is_negative
    assert partition(m).is_nonnegative
    assert partition(n).is_zero
    assert partition(p).is_positive
    assert partition(x).subs(x, 7) == 15
    assert partition(y).subs(y, 8) == 22
    raises(TypeError, lambda: partition(Rational(5, 4)))
    assert partition(9, evaluate=False) % 5 == 0
    assert partition(5*m + 4) % 5 == 0
    assert partition(47, evaluate=False) % 7 == 0
    assert partition(7*m + 5) % 7 == 0
    assert partition(50, evaluate=False) % 11 == 0
    assert partition(11*m + 6) % 11 == 0


def test_partition():
    from sympy.abc import x

    a = Partition([1, 2, 3], [4])
    b = Partition([1, 2], [3, 4])
    c = Partition([x])
    l = [a, b, c]
    l.sort(key=default_sort_key)
    assert l == [c, a, b]
    l.sort(key=lambda w: default_sort_key(w, order='rev-lex'))
    assert l == [c, a, b]

    assert (a == b) is False
    assert a <= b
    assert (a > b) is False
    assert a != b
    assert a < b

    assert (a + 2).partition == [[1, 2], [3, 4]]
    assert (b - 1).partition == [[1, 2, 4], [3]]

    assert (a - 1).partition == [[1, 2, 3, 4]]
    assert (a + 1).partition == [[1, 2, 4], [3]]
    assert (b + 1).partition == [[1, 2], [3], [4]]

    assert a.rank == 1
    assert b.rank == 3

    assert a.RGS == (0, 0, 0, 1)
    assert b.RGS == (0, 0, 1, 1)


def test_partition():
    G = nx.barbell_graph(3, 0)
    split = kernighan_lin_bisection(G)
    assert_partition_equal(split, [{0, 1, 2}, {3, 4, 5}])

