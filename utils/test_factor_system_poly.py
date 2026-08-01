
def test_factor_system_poly():

    px = lambda e: Poly(e, x)
    pxab = lambda e: Poly(e, x, domain=ZZ[a, b])
    pxI = lambda e: Poly(e, x, domain=QQ_I)
    pxyz = lambda e: Poly(e, (x, y, z))

    assert factor_system_poly([px(x**2 - 1), px(x**2 - 4)]) == [
        [px(x + 2), px(x + 1)],
        [px(x + 2), px(x - 1)],
        [px(x + 1), px(x - 2)],
        [px(x - 1), px(x - 2)],
    ]

    assert factor_system_poly([px(x**2 - 1)]) == [[px(x + 1)], [px(x - 1)]]

    assert factor_system_poly([pxyz(x**2*y - y), pxyz(x**2*z - z)]) == [
        [pxyz(x + 1)],
        [pxyz(x - 1)],
        [pxyz(y), pxyz(z)],
    ]

    assert factor_system_poly([px(x**2*(x - 1)**2), px(x*(x - 1))]) == [
        [px(x)],
        [px(x - 1)],
    ]

    assert factor_system_poly([pxyz(x**2 + y*x), pxyz(x**2 + z*x)]) == [
        [pxyz(x + y), pxyz(x + z)],
        [pxyz(x)],
    ]

    assert factor_system_poly([pxab((a - 1)*(x - 2)), pxab((b - 3)*(x - 2))]) == [
        [pxab(x - 2)],
        [pxab(a - 1), pxab(b - 3)],
    ]

    assert factor_system_poly([pxI(x**2 + 1)]) == [[pxI(x + I)], [pxI(x - I)]]

    assert factor_system_poly([]) == [[]]

    assert factor_system_poly([px(1)]) == []
    assert factor_system_poly([px(0), px(x)]) == [[px(x)]]

