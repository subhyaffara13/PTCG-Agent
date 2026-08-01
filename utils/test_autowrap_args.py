
def test_autowrap_args():
    x, y, z = symbols('x y z')

    raises(CodeGenArgumentListError, lambda: autowrap(Eq(z, x + y),
           backend='dummy', args=[x]))
    f = autowrap(Eq(z, x + y), backend='dummy', args=[y, x])
    assert f() == str(x + y)
    assert f.args == "y, x"
    assert f.returns == "z"

    raises(CodeGenArgumentListError, lambda: autowrap(Eq(z, x + y + z),
           backend='dummy', args=[x, y]))
    f = autowrap(Eq(z, x + y + z), backend='dummy', args=[y, x, z])
    assert f() == str(x + y + z)
    assert f.args == "y, x, z"
    assert f.returns == "z"

    f = autowrap(Eq(z, x + y + z), backend='dummy', args=(y, x, z))
    assert f() == str(x + y + z)
    assert f.args == "y, x, z"
    assert f.returns == "z"

