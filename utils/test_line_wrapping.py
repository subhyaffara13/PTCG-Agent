
def test_line_wrapping():
    x, y = symbols('x,y')
    assert fcode(((x + y)**10).expand(), assign_to="var") == (
        "      var = x**10 + 10*x**9*y + 45*x**8*y**2 + 120*x**7*y**3 + 210*x**6*\n"
        "     @ y**4 + 252*x**5*y**5 + 210*x**4*y**6 + 120*x**3*y**7 + 45*x**2*y\n"
        "     @ **8 + 10*x*y**9 + y**10"
    )
    e = [x**i for i in range(11)]
    assert fcode(Add(*e)) == (
        "      x**10 + x**9 + x**8 + x**7 + x**6 + x**5 + x**4 + x**3 + x**2 + x\n"
        "     @ + 1"
    )

