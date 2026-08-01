
def test_Add():
    assert precedence(x + y) == PRECEDENCE["Add"]
    assert precedence(x*y + 1) == PRECEDENCE["Add"]


def test_Add():
    sT(x + y, "Add(Symbol('x'), Symbol('y'))")
    assert srepr(x**2 + 1, order='lex') == "Add(Pow(Symbol('x'), Integer(2)), Integer(1))"
    assert srepr(x**2 + 1, order='old') == "Add(Integer(1), Pow(Symbol('x'), Integer(2)))"
    assert srepr(sympify('x + 3 - 2', evaluate=False), order='none') == "Add(Symbol('x'), Integer(3), Mul(Integer(-1), Integer(2)))"


def test_Add():
    assert str(x + y) == "x + y"
    assert str(x + 1) == "x + 1"
    assert str(x + x**2) == "x**2 + x"
    assert str(Add(0, 1, evaluate=False)) == "0 + 1"
    assert str(Add(0, 0, 1, evaluate=False)) == "0 + 0 + 1"
    assert str(1.0*x) == "1.0*x"
    assert str(5 + x + y + x*y + x**2 + y**2) == "x**2 + x*y + x + y**2 + y + 5"
    assert str(1 + x + x**2/2 + x**3/3) == "x**3/3 + x**2/2 + x + 1"
    assert str(2*x - 7*x**2 + 2 + 3*y) == "-7*x**2 + 2*x + 3*y + 2"
    assert str(x - y) == "x - y"
    assert str(2 - x) == "2 - x"
    assert str(x - 2) == "x - 2"
    assert str(x - y - z - w) == "-w + x - y - z"
    assert str(x - z*y**2*z*w) == "-w*y**2*z**2 + x"
    assert str(x - 1*y*x*y) == "-x*y**2 + x"
    assert str(sin(x).series(x, 0, 15)) == "x - x**3/6 + x**5/120 - x**7/5040 + x**9/362880 - x**11/39916800 + x**13/6227020800 + O(x**15)"
    assert str(Add(Add(-w, x, evaluate=False), Add(-y, z,  evaluate=False),  evaluate=False)) == "(-w + x) + (-y + z)"
    assert str(Add(Add(-x, -y, evaluate=False), -z, evaluate=False)) == "-z + (-x - y)"
    assert str(Add(Add(Add(-x, -y, evaluate=False), -z, evaluate=False), -t, evaluate=False)) == "-t + (-z + (-x - y))"

