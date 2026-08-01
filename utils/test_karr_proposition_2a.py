
def test_karr_proposition_2a():
    # Test Karr, page 309, proposition 2, part a
    i, u, v = symbols('i u v', integer=True)

    def test_the_product(m, n):
        # g
        g = i**3 + 2*i**2 - 3*i
        # f = Delta g
        f = simplify(g.subs(i, i+1) / g)
        # The product
        a = m
        b = n - 1
        P = Product(f, (i, a, b)).doit()
        # Test if Product_{m <= i < n} f(i) = g(n) / g(m)
        assert combsimp(P / (g.subs(i, n) / g.subs(i, m))) == 1

    # m < n
    test_the_product(u, u + v)
    # m = n
    test_the_product(u, u)
    # m > n
    test_the_product(u + v, u)


def test_karr_proposition_2a():
    # Test Karr, page 309, proposition 2, part a
    i = Symbol("i", integer=True)
    u = Symbol("u", integer=True)
    v = Symbol("v", integer=True)

    def test_the_sum(m, n):
        # g
        g = i**3 + 2*i**2 - 3*i
        # f = Delta g
        f = simplify(g.subs(i, i+1) - g)
        # The sum
        a = m
        b = n - 1
        S = Sum(f, (i, a, b)).doit()
        # Test if Sum_{m <= i < n} f(i) = g(n) - g(m)
        assert simplify(S - (g.subs(i, n) - g.subs(i, m))) == 0

    # m < n
    test_the_sum(u,   u+v)
    # m = n
    test_the_sum(u,   u  )
    # m > n
    test_the_sum(u+v, u  )

