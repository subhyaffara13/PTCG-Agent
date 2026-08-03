import random

def test_random():
    M = randMatrix(3, 3)
    M = randMatrix(3, 3, seed=3)
    assert M == randMatrix(3, 3, seed=3)

    M = randMatrix(3, 4, 0, 150)
    M = randMatrix(3, seed=4, symmetric=True)
    assert M == randMatrix(3, seed=4, symmetric=True)

    S = M.copy()
    S.simplify()
    assert S == M  # doesn't fail when elements are Numbers, not int

    rng = random.Random(4)
    assert M == randMatrix(3, symmetric=True, prng=rng)

    # Ensure symmetry
    for size in (10, 11): # Test odd and even
        for percent in (100, 70, 30):
            M = randMatrix(size, symmetric=True, percent=percent, prng=rng)
            assert M == M.T

    M = randMatrix(10, min=1, percent=70)
    zero_count = 0
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] == 0:
                zero_count += 1
    assert zero_count == 30


def test_random():
    M = randMatrix(3, 3)
    M = randMatrix(3, 3, seed=3)
    assert M == randMatrix(3, 3, seed=3)

    M = randMatrix(3, 4, 0, 150)
    M = randMatrix(3, seed=4, symmetric=True)
    assert M == randMatrix(3, seed=4, symmetric=True)

    S = M.copy()
    S.simplify()
    assert S == M  # doesn't fail when elements are Numbers, not int

    rng = random.Random(4)
    assert M == randMatrix(3, symmetric=True, prng=rng)

    # Ensure symmetry
    for size in (10, 11): # Test odd and even
        for percent in (100, 70, 30):
            M = randMatrix(size, symmetric=True, percent=percent, prng=rng)
            assert M == M.T

    M = randMatrix(10, min=1, percent=70)
    zero_count = 0
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if M[i, j] == 0:
                zero_count += 1
    assert zero_count == 30


def test_random():
    from sympy.functions.combinatorial.numbers import lucas
    from sympy.simplify.simplify import posify
    assert posify(x)[0]._random() is not None
    assert lucas(n)._random(2, -2, 0, -1, 1) is None

    # issue 8662
    assert Piecewise((Max(x, y), z))._random() is None


def test_random():
    random.seed(42)
    a = random.random()
    random.seed(42)
    Symbol('z').is_finite
    b = random.random()
    assert a == b

    got = set()
    for i in range(2):
        random.seed(28)
        m0, m1 = symbols('m_0 m_1', real=True)
        _ = acos(-m0/m1)
        got.add(random.uniform(0,1))
    assert len(got) == 1

    random.seed(10)
    y = 0
    for i in range(4):
        y += sin(random.uniform(-10,10) * x)
    random.seed(10)
    z = 0
    for i in range(4):
        z += sin(random.uniform(-10,10) * x)
    assert y == z

