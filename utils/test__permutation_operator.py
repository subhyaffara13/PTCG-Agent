
def test_PermutationOperator():
    p, q, r, s = symbols('p,q,r,s')
    f, g, h, i = map(Function, 'fghi')
    P = PermutationOperator
    assert P(p, q).get_permuted(f(p)*g(q)) == -f(q)*g(p)
    assert P(p, q).get_permuted(f(p, q)) == -f(q, p)
    assert P(p, q).get_permuted(f(p)) == f(p)
    expr = (f(p)*g(q)*h(r)*i(s)
        - f(q)*g(p)*h(r)*i(s)
        - f(p)*g(q)*h(s)*i(r)
        + f(q)*g(p)*h(s)*i(r))
    perms = [P(p, q), P(r, s)]
    assert (simplify_index_permutations(expr, perms) ==
        P(p, q)*P(r, s)*f(p)*g(q)*h(r)*i(s))
    assert latex(P(p, q)) == 'P(pq)'

    p1, p2 = symbols('p1,p2')
    assert latex(P(p1,p2) == 'P(p_{1}p_{2})')

