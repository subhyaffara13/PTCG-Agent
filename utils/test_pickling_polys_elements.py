
def test_pickling_polys_elements():
    from sympy.polys.domains.pythonrational import PythonRational
    #from sympy.polys.domains.pythonfinitefield import PythonFiniteField
    #from sympy.polys.domains.mpelements import MPContext

    for c in (PythonRational, PythonRational(1, 7)):
        check(c)

