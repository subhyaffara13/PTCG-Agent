
def test_fresnel_integrals_scipy():
    if not scipy:
        skip("scipy not installed")

    f1 = fresnelc(x)
    f2 = fresnels(x)
    F1 = lambdify(x, f1, modules='scipy')
    F2 = lambdify(x, f2, modules='scipy')

    assert abs(fresnelc(1.3) - F1(1.3)) <= 1e-10
    assert abs(fresnels(1.3) - F2(1.3)) <= 1e-10

