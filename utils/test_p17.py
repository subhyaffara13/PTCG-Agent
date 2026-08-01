
def test_P17():
    t = symbols('t', real=True)
    M=Matrix([
        [sin(2*t), cos(2*t)],
        [2*(1 - (cos(t)**2))*cos(t), (1 - 2*(sin(t)**2))*sin(t)]])
    assert M.rank() == 1

