
def test_roots_quintic():
    eqs = (x**5 - 2,
            (x/2 + 1)**5 - 5*(x/2 + 1) + 12,
            x**5 - 110*x**3 - 55*x**2 + 2310*x + 979)
    for eq in eqs:
        roots = roots_quintic(Poly(eq))
        assert len(roots) == 5
        assert all(eq.subs(x, r.n(10)).n(chop = 1e-5) == 0 for r in roots)

