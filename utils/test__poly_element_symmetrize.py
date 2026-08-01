
def test_PolyElement_symmetrize():
    R, x, y = ring("x,y", ZZ)

    # Homogeneous, symmetric
    f = x**2 + y**2
    sym, rem, m = f.symmetrize()
    assert rem == 0
    assert sym.compose(m) + rem == f

    # Homogeneous, asymmetric
    f = x**2 - y**2
    sym, rem, m = f.symmetrize()
    assert rem != 0
    assert sym.compose(m) + rem == f

    # Inhomogeneous, symmetric
    f = x*y + 7
    sym, rem, m = f.symmetrize()
    assert rem == 0
    assert sym.compose(m) + rem == f

    # Inhomogeneous, asymmetric
    f = y + 7
    sym, rem, m = f.symmetrize()
    assert rem != 0
    assert sym.compose(m) + rem == f

    # Constant
    f = R.from_expr(3)
    sym, rem, m = f.symmetrize()
    assert rem == 0
    assert sym.compose(m) + rem == f

    # Constant constructed from sring
    R, f = sring(3)
    sym, rem, m = f.symmetrize()
    assert rem == 0
    assert sym.compose(m) + rem == f

