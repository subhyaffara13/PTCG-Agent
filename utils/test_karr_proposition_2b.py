
def test_karr_proposition_2b():
    # Test Karr, page 309, proposition 2, part b
    i, u, v, w = symbols('i u v w', integer=True)

    def test_the_product(l, n, m):
        # Productmand
        s = i**3
        # First product
        a = l
        b = n - 1
        S1 = Product(s, (i, a, b)).doit()
        # Second product
        a = l
        b = m - 1
        S2 = Product(s, (i, a, b)).doit()
        # Third product
        a = m
        b = n - 1
        S3 = Product(s, (i, a, b)).doit()
        # Test if S1 = S2 * S3 as required
        assert combsimp(S1 / (S2 * S3)) == 1

    # l < m < n
    test_the_product(u, u + v, u + v + w)
    # l < m = n
    test_the_product(u, u + v, u + v)
    # l < m > n
    test_the_product(u, u + v + w, v)
    # l = m < n
    test_the_product(u, u, u + v)
    # l = m = n
    test_the_product(u, u, u)
    # l = m > n
    test_the_product(u + v, u + v, u)
    # l > m < n
    test_the_product(u + v, u, u + w)
    # l > m = n
    test_the_product(u + v, u, u)
    # l > m > n
    test_the_product(u + v + w, u + v, u)


def test_karr_proposition_2b():
    # Test Karr, page 309, proposition 2, part b
    i = Symbol("i", integer=True)
    u = Symbol("u", integer=True)
    v = Symbol("v", integer=True)
    w = Symbol("w", integer=True)

    def test_the_sum(l, n, m):
        # Summand
        s = i**3
        # First sum
        a = l
        b = n - 1
        S1 = Sum(s, (i, a, b)).doit()
        # Second sum
        a = l
        b = m - 1
        S2 = Sum(s, (i, a, b)).doit()
        # Third sum
        a = m
        b = n - 1
        S3 = Sum(s, (i, a, b)).doit()
        # Test if S1 = S2 + S3 as required
        assert S1 - (S2 + S3) == 0

    # l < m < n
    test_the_sum(u,     u+v,   u+v+w)
    # l < m = n
    test_the_sum(u,     u+v,   u+v  )
    # l < m > n
    test_the_sum(u,     u+v+w, v    )
    # l = m < n
    test_the_sum(u,     u,     u+v  )
    # l = m = n
    test_the_sum(u,     u,     u    )
    # l = m > n
    test_the_sum(u+v,   u+v,   u    )
    # l > m < n
    test_the_sum(u+v,   u,     u+w  )
    # l > m = n
    test_the_sum(u+v,   u,     u    )
    # l > m > n
    test_the_sum(u+v+w, u+v,   u    )

