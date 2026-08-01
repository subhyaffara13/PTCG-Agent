
def test_sring():
    x, y, z, t = symbols("x,y,z,t")

    R = PolyRing("x,y,z", ZZ, lex)
    assert sring(x + 2*y + 3*z) == (R, R.x + 2*R.y + 3*R.z)

    R = PolyRing("x,y,z", QQ, lex)
    assert sring(x + 2*y + z/3) == (R, R.x + 2*R.y + R.z/3)
    assert sring([x, 2*y, z/3]) == (R, [R.x, 2*R.y, R.z/3])

    Rt = PolyRing("t", ZZ, lex)
    R = PolyRing("x,y,z", Rt, lex)
    assert sring(x + 2*t*y + 3*t**2*z, x, y, z) == (R, R.x + 2*Rt.t*R.y + 3*Rt.t**2*R.z)

    Rt = PolyRing("t", QQ, lex)
    R = PolyRing("x,y,z", Rt, lex)
    assert sring(x + t*y/2 + t**2*z/3, x, y, z) == (R, R.x + Rt.t*R.y/2 + Rt.t**2*R.z/3)

    Rt = FracField("t", ZZ, lex)
    R = PolyRing("x,y,z", Rt, lex)
    assert sring(x + 2*y/t + t**2*z/3, x, y, z) == (R, R.x + 2*R.y/Rt.t + Rt.t**2*R.z/3)

    r = sqrt(2) - sqrt(3)
    R, a = sring(r, extension=True)
    assert R.domain == QQ.algebraic_field(sqrt(2) + sqrt(3))
    assert R.gens == ()
    assert a == R.domain.from_sympy(r)

