
def test_2arg_hack():
    N = Symbol('N', commutative=False)
    ans = Mul(2, y + 1, evaluate=False)
    assert (2*x*(y + 1)).subs(x, 1, hack2=True) == ans
    assert (2*(y + 1 + N)).subs(N, 0, hack2=True) == ans

