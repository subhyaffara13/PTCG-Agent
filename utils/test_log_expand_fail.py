
def test_log_expand_fail():
    x, y, z = symbols('x,y,z', positive=True)
    assert (log(x*(y + z))*(x + y)).expand(mul=True, log=True) == y*log(
        x) + y*log(y + z) + z*log(x) + z*log(y + z)

