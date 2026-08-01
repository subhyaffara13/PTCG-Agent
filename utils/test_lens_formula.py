
def test_lens_formula():
    u, v, f = symbols('u, v, f')
    assert lens_formula(focal_length=f, u=u) == f*u/(f + u)
    assert lens_formula(focal_length=f, v=v) == f*v/(f - v)
    assert lens_formula(u=u, v=v) == u*v/(u - v)
    assert lens_formula(u=oo, v=v) == v
    assert lens_formula(u=oo, v=oo) is oo
    assert lens_formula(focal_length=oo, u=u) == u
    assert lens_formula(u=u, v=oo) == -u
    assert lens_formula(focal_length=oo, v=oo) is -oo
    assert lens_formula(focal_length=oo, v=v) == v
    assert lens_formula(focal_length=f, v=oo) == -f
    assert lens_formula(focal_length=oo, u=oo) is oo
    assert lens_formula(focal_length=oo, u=u) == u
    assert lens_formula(focal_length=f, u=oo) == f
    raises(ValueError, lambda: lens_formula(focal_length=f, u=u, v=v))

