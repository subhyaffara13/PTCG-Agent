
def test_W24():
    # Not that slow, but does not fully evaluate so simplify is slow.
    # Maybe also require doit()
    x, y = symbols('x y', real=True)
    r1 = integrate(integrate(sqrt(x**2 + y**2), (x, 0, 1)), (y, 0, 1))
    assert (r1 - (sqrt(2) + asinh(1))/3).simplify() == 0

