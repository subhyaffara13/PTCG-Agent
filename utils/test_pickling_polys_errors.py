
def test_pickling_polys_errors():
    from sympy.polys.polyerrors import (HeuristicGCDFailed,
        HomomorphismFailed, IsomorphismFailed, ExtraneousFactors,
        EvaluationFailed, RefinementFailed, CoercionFailed, NotInvertible,
        NotReversible, NotAlgebraic, DomainError, PolynomialError,
        UnificationFailed, GeneratorsError, GeneratorsNeeded,
        UnivariatePolynomialError, MultivariatePolynomialError, OptionError,
        FlagError)
    # from sympy.polys.polyerrors import (ExactQuotientFailed,
    #         OperationNotSupported, ComputationFailed, PolificationFailed)

    # x = Symbol('x')

    # TODO: TypeError: __init__() takes at least 3 arguments (1 given)
    # for c in (ExactQuotientFailed, ExactQuotientFailed(x, 3*x, ZZ)):
    #    check(c)

    # TODO: TypeError: can't pickle instancemethod objects
    # for c in (OperationNotSupported, OperationNotSupported(Poly(x), Poly.gcd)):
    #    check(c)

    for c in (HeuristicGCDFailed, HeuristicGCDFailed()):
        check(c)

    for c in (HomomorphismFailed, HomomorphismFailed()):
        check(c)

    for c in (IsomorphismFailed, IsomorphismFailed()):
        check(c)

    for c in (ExtraneousFactors, ExtraneousFactors()):
        check(c)

    for c in (EvaluationFailed, EvaluationFailed()):
        check(c)

    for c in (RefinementFailed, RefinementFailed()):
        check(c)

    for c in (CoercionFailed, CoercionFailed()):
        check(c)

    for c in (NotInvertible, NotInvertible()):
        check(c)

    for c in (NotReversible, NotReversible()):
        check(c)

    for c in (NotAlgebraic, NotAlgebraic()):
        check(c)

    for c in (DomainError, DomainError()):
        check(c)

    for c in (PolynomialError, PolynomialError()):
        check(c)

    for c in (UnificationFailed, UnificationFailed()):
        check(c)

    for c in (GeneratorsError, GeneratorsError()):
        check(c)

    for c in (GeneratorsNeeded, GeneratorsNeeded()):
        check(c)

    # TODO: PicklingError: Can't pickle <function <lambda> at 0x38578c0>: it's not found as __main__.<lambda>
    # for c in (ComputationFailed, ComputationFailed(lambda t: t, 3, None)):
    #    check(c)

    for c in (UnivariatePolynomialError, UnivariatePolynomialError()):
        check(c)

    for c in (MultivariatePolynomialError, MultivariatePolynomialError()):
        check(c)

    # TODO: TypeError: __init__() takes at least 3 arguments (1 given)
    # for c in (PolificationFailed, PolificationFailed({}, x, x, False)):
    #    check(c)

    for c in (OptionError, OptionError()):
        check(c)

    for c in (FlagError, FlagError()):
        check(c)

