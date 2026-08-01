
def test_Derivative():
    with ignore_warnings(UserWarning):
        simp = lambda expr: aesara_simplify(fgraph_of(expr))
        assert theq(simp(aesara_code_(sy.Derivative(sy.sin(x), x, evaluate=False))),
                    simp(aesara.grad(aet.sin(xt), xt)))


def test_Derivative():
    assert mcode(Derivative(sin(x), x)) == "Hold[D[Sin[x], x]]"
    assert mcode(Derivative(x, x)) == "Hold[D[x, x]]"
    assert mcode(Derivative(sin(x)*y**4, x, 2)) == "Hold[D[y^4*Sin[x], {x, 2}]]"
    assert mcode(Derivative(sin(x)*y**4, x, y, x)) == "Hold[D[y^4*Sin[x], x, y, x]]"
    assert mcode(Derivative(sin(x)*y**4, x, y, 3, x)) == "Hold[D[y^4*Sin[x], x, {y, 3}, x]]"


def test_Derivative():
    assert precedence(Derivative(x, y)) == PRECEDENCE["Atom"]


def test_Derivative():
    assert str(Derivative(x, y)) == "Derivative(x, y)"
    assert str(Derivative(x**2, x, evaluate=False)) == "Derivative(x**2, x)"
    assert str(Derivative(
        x**2/y, x, y, evaluate=False)) == "Derivative(x**2/y, x, y)"


def test_Derivative():
    simp = lambda expr: theano_simplify(fgraph_of(expr))
    assert theq(simp(theano_code_(sy.Derivative(sy.sin(x), x, evaluate=False))),
                simp(theano.grad(tt.sin(xt), xt)))

