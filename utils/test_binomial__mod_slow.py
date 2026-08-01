
def test_binomial_Mod_slow():
    p, q = 10**5 + 3, 10**9 + 33 # prime modulo
    r, s = 10**7 + 5, 33333333 # composite modulo

    n, k, m = symbols('n k m')
    assert (binomial(n, k) % q).subs({n: s, k: p}) == Mod(binomial(s, p), q)
    assert (binomial(n, k) % m).subs({n: 8, k: 5, m: 13}) == 4
    assert (binomial(9, k) % 7).subs(k, 2) == 1

    # Lucas Theorem
    assert Mod(binomial(123456, 43253, evaluate=False), p) == Mod(binomial(123456, 43253), p)
    assert Mod(binomial(-178911, 237, evaluate=False), p) == Mod(-binomial(178911 + 237 - 1, 237), p)
    assert Mod(binomial(-178911, 238, evaluate=False), p) == Mod(binomial(178911 + 238 - 1, 238), p)

    # factorial Mod
    assert Mod(binomial(9734, 451, evaluate=False), q) == Mod(binomial(9734, 451), q)
    assert Mod(binomial(-10733, 4459, evaluate=False), q) == Mod(binomial(-10733, 4459), q)
    assert Mod(binomial(-15733, 4458, evaluate=False), q) == Mod(binomial(-15733, 4458), q)
    assert Mod(binomial(23, -38, evaluate=False), q) is S.Zero
    assert Mod(binomial(23, 38, evaluate=False), q) is S.Zero

    # binomial factorize
    assert Mod(binomial(753, 119, evaluate=False), r) == Mod(binomial(753, 119), r)
    assert Mod(binomial(3781, 948, evaluate=False), s) == Mod(binomial(3781, 948), s)
    assert Mod(binomial(25773, 1793, evaluate=False), s) == Mod(binomial(25773, 1793), s)
    assert Mod(binomial(-753, 118, evaluate=False), r) == Mod(binomial(-753, 118), r)
    assert Mod(binomial(-25773, 1793, evaluate=False), s) == Mod(binomial(-25773, 1793), s)

