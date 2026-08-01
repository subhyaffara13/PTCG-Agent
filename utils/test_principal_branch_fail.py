
def test_principal_branch_fail():
    # TODO XXX why does abs(x)._eval_evalf() not fall back to global evalf?
    from sympy.functions.elementary.complexes import principal_branch
    assert N_equals(principal_branch((1 + I)**2, pi/2), 0)

