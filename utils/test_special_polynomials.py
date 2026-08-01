
def test_special_polynomials():
    assert mcode(hermite(x, y)) == "HermiteH[x, y]"
    assert mcode(laguerre(x, y)) == "LaguerreL[x, y]"
    assert mcode(assoc_laguerre(x, y, z)) == "LaguerreL[x, y, z]"
    assert mcode(jacobi(x, y, z, w)) == "JacobiP[x, y, z, w]"
    assert mcode(gegenbauer(x, y, z)) == "GegenbauerC[x, y, z]"
    assert mcode(chebyshevt(x, y)) == "ChebyshevT[x, y]"
    assert mcode(chebyshevu(x, y)) == "ChebyshevU[x, y]"
    assert mcode(legendre(x, y)) == "LegendreP[x, y]"
    assert mcode(assoc_legendre(x, y, z)) == "LegendreP[x, y, z]"

