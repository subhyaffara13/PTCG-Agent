
def test_mirror_formula():
    u, v, f = symbols('u, v, f')
    assert mirror_formula(focal_length=f, u=u) == f*u/(-f + u)
    assert mirror_formula(focal_length=f, v=v) == f*v/(-f + v)
    assert mirror_formula(u=u, v=v) == u*v/(u + v)
    assert mirror_formula(u=oo, v=v) == v
    assert mirror_formula(u=oo, v=oo) is oo
    assert mirror_formula(focal_length=oo, u=u) == -u
    assert mirror_formula(u=u, v=oo) == u
    assert mirror_formula(focal_length=oo, v=oo) is oo
    assert mirror_formula(focal_length=f, v=oo) == f
    assert mirror_formula(focal_length=oo, v=v) == -v
    assert mirror_formula(focal_length=oo, u=oo) is oo
    assert mirror_formula(focal_length=f, u=oo) == f
    assert mirror_formula(focal_length=oo, u=u) == -u
    raises(ValueError, lambda: mirror_formula(focal_length=f, u=u, v=v))

