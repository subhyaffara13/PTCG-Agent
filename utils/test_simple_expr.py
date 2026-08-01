
def test_simple_expr():
    e = a + 1.0
    f = g.llvm_callable([a], e)
    res = float(e.subs({a: 4.0}).evalf())
    jit_res = f(4.0)

    assert isclose(jit_res, res)

