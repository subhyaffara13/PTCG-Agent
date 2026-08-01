
def test_evaluate_false():
    # Previously this failed because the assumptions query would make new
    # expressions and some of the evaluation logic would fail under
    # evaluate(False).
    from sympy.core.parameters import evaluate
    from sympy.abc import x, h
    f = 2**x**7
    with evaluate(False):
        fh = f.xreplace({x: x+h})
        assert fh.exp.is_rational is None


def test_evaluate_false():
    for no in [0, False]:
        assert Add(3, 2, evaluate=no).is_Add
        assert Mul(3, 2, evaluate=no).is_Mul
        assert Pow(3, 2, evaluate=no).is_Pow
    assert Pow(y, 2, evaluate=True) - Pow(y, 2, evaluate=True) == 0


def test_evaluate_false():
    cases = {
        '2 + 3': Add(2, 3, evaluate=False),
        '2**2 / 3': Mul(Pow(2, 2, evaluate=False), Pow(3, -1, evaluate=False), evaluate=False),
        '2 + 3 * 5': Add(2, Mul(3, 5, evaluate=False), evaluate=False),
        '2 - 3 * 5': Add(2, Mul(-1, Mul(3, 5,evaluate=False), evaluate=False), evaluate=False),
        '1 / 3': Mul(1, Pow(3, -1, evaluate=False), evaluate=False),
        'True | False': Or(True, False, evaluate=False),
        '1 + 2 + 3 + 5*3 + integrate(x)': Add(1, 2, 3, Mul(5, 3, evaluate=False), x**2/2, evaluate=False),
        '2 * 4 * 6 + 8': Add(Mul(2, 4, 6, evaluate=False), 8, evaluate=False),
        '2 - 8 / 4': Add(2, Mul(-1, Mul(8, Pow(4, -1, evaluate=False), evaluate=False), evaluate=False), evaluate=False),
        '2 - 2**2': Add(2, Mul(-1, Pow(2, 2, evaluate=False), evaluate=False), evaluate=False),
    }
    for case, result in cases.items():
        assert sympify(case, evaluate=False) == result

