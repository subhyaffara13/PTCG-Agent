
def test_deprecated_get_segments(adaptive):
    if not matplotlib:
        skip("Matplotlib not the default backend")

    x = Symbol('x')
    f = sin(x)
    p = plot(f, (x, -10, 10), show=False, adaptive=adaptive, n=10)
    with warns_deprecated_sympy():
        p[0].get_segments()

