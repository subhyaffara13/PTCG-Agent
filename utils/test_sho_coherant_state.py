
def test_sho_coherant_state():
    alpha = Symbol('alpha', is_complex=True)
    cstate = exp(-Abs(alpha)**2/S(2))*Sum(((alpha**p)/sqrt(factorial(p)))*SHOKet(p), (p,0,oo))
    # Projection onto the number eigenstate
    assert qapply(SHOBra(q)*cstate, sum_doit=True) == exp(-Abs(alpha)**2/S(2))*alpha**q/sqrt(factorial(q))
    # Ensure that the coherent state is an eigenstate of annihilation operator
    assert simplify(qapply(SHOBra(q)*a*cstate, sum_doit=True)) == simplify(qapply(SHOBra(q)*alpha*cstate, sum_doit=True))

