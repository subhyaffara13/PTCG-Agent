
def test_sqf_norm():
    assert sqf_norm(x**2 - 2, extension=sqrt(3)) == \
        ([1], x**2 - 2*sqrt(3)*x + 1, x**4 - 10*x**2 + 1)
    assert sqf_norm(x**2 - 3, extension=sqrt(2)) == \
        ([1], x**2 - 2*sqrt(2)*x - 1, x**4 - 10*x**2 + 1)

    assert Poly(x**2 - 2, extension=sqrt(3)).sqf_norm() == \
        ([1], Poly(x**2 - 2*sqrt(3)*x + 1, x, extension=sqrt(3)),
              Poly(x**4 - 10*x**2 + 1, x, domain='QQ'))

    assert Poly(x**2 - 3, extension=sqrt(2)).sqf_norm() == \
        ([1], Poly(x**2 - 2*sqrt(2)*x - 1, x, extension=sqrt(2)),
              Poly(x**4 - 10*x**2 + 1, x, domain='QQ'))

