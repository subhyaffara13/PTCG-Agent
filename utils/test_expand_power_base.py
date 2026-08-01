
def test_expand_power_base():
    assert expand_power_base((x*y*z)**4) == x**4*y**4*z**4
    assert expand_power_base((x*y*z)**x).is_Pow
    assert expand_power_base((x*y*z)**x, force=True) == x**x*y**x*z**x
    assert expand_power_base((x*(y*z)**2)**3) == x**3*y**6*z**6

    assert expand_power_base((sin((x*y)**2)*y)**z).is_Pow
    assert expand_power_base(
        (sin((x*y)**2)*y)**z, force=True) == sin((x*y)**2)**z*y**z
    assert expand_power_base(
        (sin((x*y)**2)*y)**z, deep=True) == (sin(x**2*y**2)*y)**z

    assert expand_power_base(exp(x)**2) == exp(2*x)
    assert expand_power_base((exp(x)*exp(y))**2) == exp(2*x)*exp(2*y)

    assert expand_power_base(
        (exp((x*y)**z)*exp(y))**2) == exp(2*(x*y)**z)*exp(2*y)
    assert expand_power_base((exp((x*y)**z)*exp(
        y))**2, deep=True, force=True) == exp(2*x**z*y**z)*exp(2*y)

    assert expand_power_base((exp(x)*exp(y))**z).is_Pow
    assert expand_power_base(
        (exp(x)*exp(y))**z, force=True) == exp(x)**z*exp(y)**z

