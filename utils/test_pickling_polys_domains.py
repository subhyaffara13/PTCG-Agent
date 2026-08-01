
def test_pickling_polys_domains():
    # from sympy.polys.domains.pythonfinitefield import PythonFiniteField
    from sympy.polys.domains.pythonintegerring import PythonIntegerRing
    from sympy.polys.domains.pythonrationalfield import PythonRationalField

    # TODO: fix pickling of ModularInteger
    # for c in (PythonFiniteField, PythonFiniteField(17)):
    #     check(c)

    for c in (PythonIntegerRing, PythonIntegerRing()):
        check(c, check_attr=False)

    for c in (PythonRationalField, PythonRationalField()):
        check(c, check_attr=False)

    if _gmpy is not None:
        # from sympy.polys.domains.gmpyfinitefield import GMPYFiniteField
        from sympy.polys.domains.gmpyintegerring import GMPYIntegerRing
        from sympy.polys.domains.gmpyrationalfield import GMPYRationalField

        # TODO: fix pickling of ModularInteger
        # for c in (GMPYFiniteField, GMPYFiniteField(17)):
        #     check(c)

        for c in (GMPYIntegerRing, GMPYIntegerRing()):
            check(c, check_attr=False)

        for c in (GMPYRationalField, GMPYRationalField()):
            check(c, check_attr=False)

    #from sympy.polys.domains.realfield import RealField
    #from sympy.polys.domains.complexfield import ComplexField
    from sympy.polys.domains.algebraicfield import AlgebraicField
    #from sympy.polys.domains.polynomialring import PolynomialRing
    #from sympy.polys.domains.fractionfield import FractionField
    from sympy.polys.domains.expressiondomain import ExpressionDomain

    # TODO: fix pickling of RealElement
    # for c in (RealField, RealField(100)):
    #     check(c)

    # TODO: fix pickling of ComplexElement
    # for c in (ComplexField, ComplexField(100)):
    #     check(c)

    for c in (AlgebraicField, AlgebraicField(QQ, sqrt(3))):
        check(c, check_attr=False)

    # TODO: AssertionError
    # for c in (PolynomialRing, PolynomialRing(ZZ, "x,y,z")):
    #     check(c)

    # TODO: AttributeError: 'PolyElement' object has no attribute 'ring'
    # for c in (FractionField, FractionField(ZZ, "x,y,z")):
    #     check(c)

    for c in (ExpressionDomain, ExpressionDomain()):
        check(c, check_attr=False)

