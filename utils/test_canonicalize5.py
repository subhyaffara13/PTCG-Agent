
def test_canonicalize5():
    R3 = TensorIndexType('R3', dim=3)
    p = tensor_indices("p", R3)
    K = TensorHead("K", [R3])
    f = symbols("f", cls=Function)
    x = symbols("x")

    expr = integrate(f(x), (x,0,1)) * K(p)
    assert expr.as_dummy().canon_bp() == integrate(f(x), (x,0,1)).as_dummy() * K(p)

