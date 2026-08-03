import math


def test_own_module():
    f = lambdify(x, sin(x), math)
    assert f(0) == 0.0

    p, q, r = symbols("p q r", real=True)
    ae = abs(exp(p+UnevaluatedExpr(q+r)))
    f = lambdify([p, q, r], [ae, ae], modules=math)
    results = f(1.0, 1e18, -1e18)
    refvals = [math.exp(1.0)]*2
    for res, ref in zip(results, refvals):
        assert abs((res-ref)/ref) < 1e-15

