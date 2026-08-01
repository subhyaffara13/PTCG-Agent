
def test_eval_power():
    from sympy.core import Pow
    from sympy.core.expr import unchanged
    O = Operator('O')
    U = UnitaryOperator('U')
    H = HermitianOperator('H')
    assert O**-1 == O.inv() # same as doc test
    assert U**-1 == U.inv()
    assert H**-1 == H.inv()
    x = symbols("x", commutative = True)
    assert unchanged(Pow, H, x) # verify Pow(H,x)=="X^n"
    assert H**x == Pow(H, x)
    assert Pow(H,x) == Pow(H, x, evaluate=False) # Just check
    from sympy.physics.quantum.gate import XGate
    X = XGate(0) # is hermitian and unitary
    assert unchanged(Pow, X, x) # verify Pow(X,x)=="X^x"
    assert X**x == Pow(X, x)
    assert Pow(X, x, evaluate=False) == Pow(X, x) # Just check
    n = symbols("n", integer=True, even=True)
    assert X**n == 1
    n = symbols("n", integer=True, odd=True)
    assert X**n == X
    n = symbols("n", integer=True)
    assert unchanged(Pow, X, n) # verify Pow(X,n)=="X^n"
    assert X**n == Pow(X, n)
    assert Pow(X, n, evaluate=False)==Pow(X, n) # Just check
    assert X**4 == 1
    assert X**7 == X

