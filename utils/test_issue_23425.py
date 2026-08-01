
def test_issue_23425():
    x = symbols('x')
    y = Function('y')
    eq = Eq(-E**x*y(x).diff().diff() + y(x).diff(), 0)
    assert classify_ode(eq) == \
        ('Liouville', 'nth_order_reducible', \
        '2nd_power_series_ordinary', 'Liouville_Integral')

