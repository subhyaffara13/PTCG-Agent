
def test_issue_21890():
    e = S(2)/3
    assert nonlinsolve([4*x**3*y**4 - 2*y, 4*x**4*y**3 - 2*x], x, y) == {
        (2**e/(2*y), y), ((-2**e/4 - 2**e*sqrt(3)*I/4)/y, y),
        ((-2**e/4 + 2**e*sqrt(3)*I/4)/y, y)}
    assert nonlinsolve([(1 - 4*x**2)*exp(-2*x**2 - 2*y**2),
        -4*x*y*exp(-2*x**2)*exp(-2*y**2)], x, y) == {(-S(1)/2, 0), (S(1)/2, 0)}
    rx, ry = symbols('x y', real=True)
    sol = nonlinsolve([4*rx**3*ry**4 - 2*ry, 4*rx**4*ry**3 - 2*rx], rx, ry)
    ans = {(2**(S(2)/3)/(2*ry), ry),
        ((-2**(S(2)/3)/4 - 2**(S(2)/3)*sqrt(3)*I/4)/ry, ry),
        ((-2**(S(2)/3)/4 + 2**(S(2)/3)*sqrt(3)*I/4)/ry, ry)}
    assert sol == ans

