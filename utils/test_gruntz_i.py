
def test_gruntz_I():
    y = Symbol("y")
    assert gruntz(I*x, x, oo) == I*oo
    assert gruntz(y*I*x, x, oo) == y*I*oo
    assert gruntz(y*3*I*x, x, oo) == y*I*oo
    assert gruntz(y*3*sin(I)*x, x, oo) == y*I*oo

