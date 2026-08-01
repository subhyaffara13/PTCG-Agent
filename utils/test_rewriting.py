
def test_rewriting():
    from sympy.functions.elementary.piecewise import Piecewise
    assert isinstance(dirichlet_eta(x).rewrite(zeta), Piecewise)
    assert isinstance(dirichlet_eta(x).rewrite(genocchi), Piecewise)
    assert zeta(x).rewrite(dirichlet_eta) == dirichlet_eta(x)/(1 - 2**(1 - x))
    assert zeta(x).rewrite(dirichlet_eta, a=2) == zeta(x)
    assert verify_numerically(dirichlet_eta(x), dirichlet_eta(x).rewrite(zeta), x)
    assert verify_numerically(dirichlet_eta(x), dirichlet_eta(x).rewrite(genocchi), x)
    assert verify_numerically(zeta(x), zeta(x).rewrite(dirichlet_eta), x)

    assert zeta(x, a).rewrite(lerchphi) == lerchphi(1, x, a)
    assert polylog(s, z).rewrite(lerchphi) == lerchphi(z, s, 1)*z

    assert lerchphi(1, x, a).rewrite(zeta) == zeta(x, a)
    assert z*lerchphi(z, s, 1).rewrite(polylog) == polylog(s, z)


def test_rewriting():
    F, a, b = free_group("a, b")
    G = FpGroup(F, [a*b*a**-1*b**-1])
    a, b = G.generators
    R = G._rewriting_system
    assert R.is_confluent

    assert G.reduce(b**-1*a) == a*b**-1
    assert G.reduce(b**3*a**4*b**-2*a) == a**5*b
    assert G.equals(b**2*a**-1*b, b**4*a**-1*b**-1)

    assert R.reduce_using_automaton(b*a*a**2*b**-1) == a**3
    assert R.reduce_using_automaton(b**3*a**4*b**-2*a) == a**5*b
    assert R.reduce_using_automaton(b**-1*a) == a*b**-1

    G = FpGroup(F, [a**3, b**3, (a*b)**2])
    R = G._rewriting_system
    R.make_confluent()
    # R._is_confluent should be set to True after
    # a successful run of make_confluent
    assert R.is_confluent
    # but also the system should actually be confluent
    assert R._check_confluence()
    assert G.reduce(b*a**-1*b**-1*a**3*b**4*a**-1*b**-15) == a**-1*b**-1
    # check for automaton reduction
    assert R.reduce_using_automaton(b*a**-1*b**-1*a**3*b**4*a**-1*b**-15) == a**-1*b**-1

    G = FpGroup(F, [a**2, b**3, (a*b)**4])
    R = G._rewriting_system
    assert G.reduce(a**2*b**-2*a**2*b) == b**-1
    assert R.reduce_using_automaton(a**2*b**-2*a**2*b) == b**-1
    assert G.reduce(a**3*b**-2*a**2*b) == a**-1*b**-1
    assert R.reduce_using_automaton(a**3*b**-2*a**2*b) == a**-1*b**-1
    # Check after adding a rule
    R.add_rule(a**2, b)
    assert R.reduce_using_automaton(a**2*b**-2*a**2*b) == b**-1
    assert R.reduce_using_automaton(a**4*b**-2*a**2*b**3) == b

    R.set_max(15)
    raises(RuntimeError, lambda:  R.add_rule(a**-3, b))
    R.set_max(20)
    R.add_rule(a**-3, b)

    assert R.add_rule(a, a) == set()

