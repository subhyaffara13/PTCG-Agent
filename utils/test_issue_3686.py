
def test_issue_3686():  # remove this when fresnel integrals are implemented
    from sympy.core.function import expand_func
    from sympy.functions.special.error_functions import fresnels
    assert expand_func(integrate(sin(x**2), x)) == \
        sqrt(2)*sqrt(pi)*fresnels(sqrt(2)*x/sqrt(pi))/2

