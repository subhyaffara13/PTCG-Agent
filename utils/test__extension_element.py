
def test_ExtensionElement():
    A = FiniteExtension(Poly(x**2 + 1, x))
    if GROUND_TYPES != 'flint':
        ans = "ExtElem(DMP_Python([1, 0], ZZ), FiniteExtension(Poly(x**2 + 1, x, domain='ZZ')))"
    else:
        ans = "ExtElem(DUP_Flint([1, 0], ZZ), FiniteExtension(Poly(x**2 + 1, x, domain='ZZ')))"
    assert srepr(A.generator) == ans

