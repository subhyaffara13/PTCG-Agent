
def test_two_pow():
    e = a**1.5 + b**7
    f = g.llvm_callable([a, b], e)
    res = float(e.subs({a: 1.5, b: 2.0}).evalf())
    jit_res = f(1.5, 2.0)

    assert isclose(jit_res, res)

