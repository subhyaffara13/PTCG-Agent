from typing import Union

def test_solve_mul():
    assert solveset_real((a*x + b)*(exp(x) - 3), x) == \
        Union({log(3)}, Intersection({-b/a}, S.Reals))
    anz = Symbol('anz', nonzero=True)
    bb = Symbol('bb', real=True)
    assert solveset_real((anz*x + bb)*(exp(x) - 3), x) == \
        FiniteSet(-bb/anz, log(3))
    assert solveset_real((2*x + 8)*(8 + exp(x)), x) == FiniteSet(S(-4))
    assert solveset_real(x/log(x), x) is S.EmptySet

