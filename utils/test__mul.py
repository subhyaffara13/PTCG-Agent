
def test_Mul():
    e = Mul(-2, x + 1, evaluate=False)
    assert latex(e) == r'- 2 \left(x + 1\right)'
    e = Mul(2, x + 1, evaluate=False)
    assert latex(e) == r'2 \left(x + 1\right)'
    e = Mul(S.Half, x + 1, evaluate=False)
    assert latex(e) == r'\frac{x + 1}{2}'
    e = Mul(y, x + 1, evaluate=False)
    assert latex(e) == r'y \left(x + 1\right)'
    e = Mul(-y, x + 1, evaluate=False)
    assert latex(e) == r'- y \left(x + 1\right)'
    e = Mul(-2, x + 1)
    assert latex(e) == r'- 2 x - 2'
    e = Mul(2, x + 1)
    assert latex(e) == r'2 x + 2'


def test_Mul():
    A, B, C, D = symbols('A B C D', commutative=False)
    assert mcode(x*y*z) == "x*y*z"
    assert mcode(x*y*A) == "x*y*A"
    assert mcode(x*y*A*B) == "x*y*A**B"
    assert mcode(x*y*A*B*C) == "x*y*A**B**C"
    assert mcode(x*A*B*(C + D)*A*y) == "x*y*A**B**(C + D)**A"


def test_Mul():
    assert precedence(x*y) == PRECEDENCE["Mul"]
    assert precedence(-x*y) == PRECEDENCE["Add"]


def test_Mul():
    sT(3*x**3*y, "Mul(Integer(3), Pow(Symbol('x'), Integer(3)), Symbol('y'))")
    assert srepr(3*x**3*y, order='old') == "Mul(Integer(3), Symbol('y'), Pow(Symbol('x'), Integer(3)))"
    assert srepr(sympify('(x+4)*2*x*7', evaluate=False), order='none') == "Mul(Add(Symbol('x'), Integer(4)), Integer(2), Symbol('x'), Integer(7))"


def test_Mul():
    assert str(x/y) == "x/y"
    assert str(y/x) == "y/x"
    assert str(x/y/z) == "x/(y*z)"
    assert str((x + 1)/(y + 2)) == "(x + 1)/(y + 2)"
    assert str(2*x/3) == '2*x/3'
    assert str(-2*x/3) == '-2*x/3'
    assert str(-1.0*x) == '-1.0*x'
    assert str(1.0*x) == '1.0*x'
    assert str(Mul(0, 1, evaluate=False)) == '0*1'
    assert str(Mul(1, 0, evaluate=False)) == '1*0'
    assert str(Mul(1, 1, evaluate=False)) == '1*1'
    assert str(Mul(1, 1, 1, evaluate=False)) == '1*1*1'
    assert str(Mul(1, 2, evaluate=False)) == '1*2'
    assert str(Mul(1, S.Half, evaluate=False)) == '1*(1/2)'
    assert str(Mul(1, 1, S.Half, evaluate=False)) == '1*1*(1/2)'
    assert str(Mul(1, 1, 2, 3, x, evaluate=False)) == '1*1*2*3*x'
    assert str(Mul(1, -1, evaluate=False)) == '1*(-1)'
    assert str(Mul(-1, 1, evaluate=False)) == '-1*1'
    assert str(Mul(4, 3, 2, 1, 0, y, x, evaluate=False)) == '4*3*2*1*0*y*x'
    assert str(Mul(4, 3, 2, 1+z, 0, y, x, evaluate=False)) == '4*3*2*(z + 1)*0*y*x'
    assert str(Mul(Rational(2, 3), Rational(5, 7), evaluate=False)) == '(2/3)*(5/7)'
    # For issue 14160
    assert str(Mul(-2, x, Pow(Mul(y,y,evaluate=False), -1, evaluate=False),
                                                evaluate=False)) == '-2*x/(y*y)'
    # issue 21537
    assert str(Mul(x, Pow(1/y, -1, evaluate=False), evaluate=False)) == 'x/(1/y)'

    # Issue 24108
    from sympy.core.parameters import evaluate
    with evaluate(False):
        assert str(Mul(Pow(Integer(2), Integer(-1)), Add(Integer(-1), Mul(Integer(-1), Integer(1))))) == "(-1 - 1*1)/2"

    class CustomClass1(Expr):
        is_commutative = True

    class CustomClass2(Expr):
        is_commutative = True
    cc1 = CustomClass1()
    cc2 = CustomClass2()
    assert str(Rational(2)*cc1) == '2*CustomClass1()'
    assert str(cc1*Rational(2)) == '2*CustomClass1()'
    assert str(cc1*Float("1.5")) == '1.5*CustomClass1()'
    assert str(cc2*Rational(2)) == '2*CustomClass2()'
    assert str(cc2*Rational(2)*cc1) == '2*CustomClass1()*CustomClass2()'
    assert str(cc1*Rational(2)*cc2) == '2*CustomClass1()*CustomClass2()'


def test_Mul():
    expr = Mul(0, 1, evaluate=False)
    assert pretty(expr) == "0*1"
    assert upretty(expr) == "0⋅1"
    expr = Mul(1, 0, evaluate=False)
    assert pretty(expr) == "1*0"
    assert upretty(expr) == "1⋅0"
    expr = Mul(1, 1, evaluate=False)
    assert pretty(expr) == "1*1"
    assert upretty(expr) == "1⋅1"
    expr = Mul(1, 1, 1, evaluate=False)
    assert pretty(expr) == "1*1*1"
    assert upretty(expr) == "1⋅1⋅1"
    expr = Mul(1, 2, evaluate=False)
    assert pretty(expr) == "1*2"
    assert upretty(expr) == "1⋅2"
    expr = Add(0, 1, evaluate=False)
    assert pretty(expr) == "0 + 1"
    assert upretty(expr) == "0 + 1"
    expr = Mul(1, 1, 2, evaluate=False)
    assert pretty(expr) == "1*1*2"
    assert upretty(expr) == "1⋅1⋅2"
    expr = Add(0, 0, 1, evaluate=False)
    assert pretty(expr) == "0 + 0 + 1"
    assert upretty(expr) == "0 + 0 + 1"
    expr = Mul(1, -1, evaluate=False)
    assert pretty(expr) == "1*-1"
    assert upretty(expr) == "1⋅-1"
    expr = Mul(1.0, x, evaluate=False)
    assert pretty(expr) == "1.0*x"
    assert upretty(expr) == "1.0⋅x"
    expr = Mul(1, 1, 2, 3, x, evaluate=False)
    assert pretty(expr) == "1*1*2*3*x"
    assert upretty(expr) == "1⋅1⋅2⋅3⋅x"
    expr = Mul(-1, 1, evaluate=False)
    assert pretty(expr) == "-1*1"
    assert upretty(expr) == "-1⋅1"
    expr = Mul(4, 3, 2, 1, 0, y, x, evaluate=False)
    assert pretty(expr) == "4*3*2*1*0*y*x"
    assert upretty(expr) == "4⋅3⋅2⋅1⋅0⋅y⋅x"
    expr = Mul(4, 3, 2, 1+z, 0, y, x, evaluate=False)
    assert pretty(expr) == "4*3*2*(z + 1)*0*y*x"
    assert upretty(expr) == "4⋅3⋅2⋅(z + 1)⋅0⋅y⋅x"
    expr = Mul(Rational(2, 3), Rational(5, 7), evaluate=False)
    assert pretty(expr) == "2/3*5/7"
    assert upretty(expr) == "2/3⋅5/7"
    expr = Mul(x + y, Rational(1, 2), evaluate=False)
    assert pretty(expr) == "(x + y)*1/2"
    assert upretty(expr) == "(x + y)⋅1/2"
    expr = Mul(Rational(1, 2), x + y, evaluate=False)
    assert pretty(expr) == "x + y\n-----\n  2  "
    assert upretty(expr) == "x + y\n─────\n  2  "
    expr = Mul(S.One, x + y, evaluate=False)
    assert pretty(expr) == "1*(x + y)"
    assert upretty(expr) == "1⋅(x + y)"
    expr = Mul(x - y, S.One, evaluate=False)
    assert pretty(expr) == "(x - y)*1"
    assert upretty(expr) == "(x - y)⋅1"
    expr = Mul(Rational(1, 2), x - y, S.One, x + y, evaluate=False)
    assert pretty(expr) == "1/2*(x - y)*1*(x + y)"
    assert upretty(expr) == "1/2⋅(x - y)⋅1⋅(x + y)"
    expr = Mul(x + y, Rational(3, 4), S.One, y - z, evaluate=False)
    assert pretty(expr) == "(x + y)*3/4*1*(y - z)"
    assert upretty(expr) == "(x + y)⋅3/4⋅1⋅(y - z)"
    expr = Mul(x + y, Rational(1, 1), Rational(3, 4), Rational(5, 6),evaluate=False)
    assert pretty(expr) == "(x + y)*1*3/4*5/6"
    assert upretty(expr) == "(x + y)⋅1⋅3/4⋅5/6"
    expr = Mul(Rational(3, 4), x + y, S.One, y - z, evaluate=False)
    assert pretty(expr) == "3/4*(x + y)*1*(y - z)"
    assert upretty(expr) == "3/4⋅(x + y)⋅1⋅(y - z)"

