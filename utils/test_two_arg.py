
def test_two_arg():
    e = 4.0*a + b + 3.0
    f = g.llvm_callable([a, b], e)
    res = float(e.subs({a: 4.0, b: 3.0}).evalf())
    jit_res = f(4.0, 3.0)

    assert isclose(jit_res, res)

