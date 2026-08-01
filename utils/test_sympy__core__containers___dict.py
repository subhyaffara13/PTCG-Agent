
def test_sympy__core__containers__Dict():
    from sympy.core.containers import Dict
    assert _test_args(Dict({x: y, y: z}))

