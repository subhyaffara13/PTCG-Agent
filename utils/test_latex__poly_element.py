
def test_latex_PolyElement():
    Ruv, u, v = ring("u,v", ZZ)
    Rxyz, x, y, z = ring("x,y,z", Ruv)

    assert latex(x - x) == r"0"
    assert latex(x - 1) == r"x - 1"
    assert latex(x + 1) == r"x + 1"

    assert latex((u**2 + 3*u*v + 1)*x**2*y + u + 1) == \
        r"\left({u}^{2} + 3 u v + 1\right) {x}^{2} y + u + 1"
    assert latex((u**2 + 3*u*v + 1)*x**2*y + (u + 1)*x) == \
        r"\left({u}^{2} + 3 u v + 1\right) {x}^{2} y + \left(u + 1\right) x"
    assert latex((u**2 + 3*u*v + 1)*x**2*y + (u + 1)*x + 1) == \
        r"\left({u}^{2} + 3 u v + 1\right) {x}^{2} y + \left(u + 1\right) x + 1"
    assert latex((-u**2 + 3*u*v - 1)*x**2*y - (u + 1)*x - 1) == \
        r"-\left({u}^{2} - 3 u v + 1\right) {x}^{2} y - \left(u + 1\right) x - 1"

    assert latex(-(v**2 + v + 1)*x + 3*u*v + 1) == \
        r"-\left({v}^{2} + v + 1\right) x + 3 u v + 1"
    assert latex(-(v**2 + v + 1)*x - 3*u*v + 1) == \
        r"-\left({v}^{2} + v + 1\right) x - 3 u v + 1"

