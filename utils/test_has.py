
def test_has():
    a, b, c = symbols('a, b, c', cls=Dummy)
    f = Hyper_Function([2, -a], [b])
    assert f.has(a)
    assert f.has(Tuple(b))
    assert not f.has(c)


def test_has():
    assert cot(x).has(x)
    assert cot(x).has(cot)
    assert not cot(x).has(sin)
    assert sin(x).has(x)
    assert sin(x).has(sin)
    assert not sin(x).has(cot)
    assert exp(x).has(exp)


def test_has():
    A = PropertiesOnlyMatrix(((x, y), (2, 3)))
    assert A.has(x)
    assert not A.has(z)
    assert A.has(Symbol)

    A = PropertiesOnlyMatrix(((2, y), (2, 3)))
    assert not A.has(x)


def test_has():
    A = Matrix(((x, y), (2, 3)))
    assert A.has(x)
    assert not A.has(z)
    assert A.has(Symbol)

    A = A.subs(x, 2)
    assert not A.has(x)


def test_has():
    A = Matrix(((x, y), (2, 3)))
    assert A.has(x)
    assert not A.has(z)
    assert A.has(Symbol)

    A = Matrix(((2, y), (2, 3)))
    assert not A.has(x)


def test_has():
    assert b21.has(b1)
    assert b21.has(b3, b1)
    assert b21.has(Basic)
    assert not b1.has(b21, b3)
    assert not b21.has()
    assert not b21.has(str)
    assert not Symbol("x").has("x")


def test_has():
    a = Permutation([1, 0])
    G = PermutationGroup([a])
    assert G.is_abelian
    a = Permutation([2, 0, 1])
    b = Permutation([2, 1, 0])
    G = PermutationGroup([a, b])
    assert not G.is_abelian

    G = PermutationGroup([a])
    assert G.has(a)
    assert not G.has(b)

    a = Permutation([2, 0, 1, 3, 4, 5])
    b = Permutation([0, 2, 1, 3, 4])
    assert PermutationGroup(a, b).degree == \
        PermutationGroup(a, b).degree == 6

    g = PermutationGroup(Permutation(0, 2, 1))
    assert Tuple(1, g).has(g)

