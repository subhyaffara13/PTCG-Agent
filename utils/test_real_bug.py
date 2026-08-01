
def test_real_bug():
    x = Symbol("x")
    assert str(2.0*x*x) in ["(2.0*x)*x", "2.0*x**2", "2.00000000000000*x**2"]
    assert str(2.1*x*x) != "(2.0*x)*x"

