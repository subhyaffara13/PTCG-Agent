
def test_factorial_Mod():
    pr = Symbol('pr', prime=True)
    p, q = 10**9 + 9, 10**9 + 33 # prime modulo
    r, s = 10**7 + 5, 33333333 # composite modulo
    assert Mod(factorial(pr - 1), pr) == pr - 1
    assert Mod(factorial(pr - 1), -pr) == -1
    assert Mod(factorial(r - 1, evaluate=False), r) == 0
    assert Mod(factorial(s - 1, evaluate=False), s) == 0
    assert Mod(factorial(p - 1, evaluate=False), p) == p - 1
    assert Mod(factorial(q - 1, evaluate=False), q) == q - 1
    assert Mod(factorial(p - 50, evaluate=False), p) == 854928834
    assert Mod(factorial(q - 1800, evaluate=False), q) == 905504050
    assert Mod(factorial(153, evaluate=False), r) == Mod(factorial(153), r)
    assert Mod(factorial(255, evaluate=False), s) == Mod(factorial(255), s)
    assert Mod(factorial(4, evaluate=False), 3) == S.Zero
    assert Mod(factorial(5, evaluate=False), 6) == S.Zero

