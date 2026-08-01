
def test_form_1():
    symsystem1 = SymbolicSystem(states, comb_explicit_rhs,
                                alg_con=alg_con_full, output_eqns=out_eqns,
                                coord_idxs=coord_idxs, speed_idxs=speed_idxs,
                                bodies=bodies, loads=loads)

    assert symsystem1.coordinates == Matrix([x, y])
    assert symsystem1.speeds == Matrix([u, v])
    assert symsystem1.states == Matrix([x, y, u, v, lam])

    assert symsystem1.alg_con == [4]

    inter = comb_explicit_rhs
    assert simplify(symsystem1.comb_explicit_rhs - inter) == zeros(5, 1)

    assert set(symsystem1.dynamic_symbols()) == {y, v, lam, u, x}
    assert type(symsystem1.dynamic_symbols()) == tuple
    assert set(symsystem1.constant_symbols()) == {l, g, m}
    assert type(symsystem1.constant_symbols()) == tuple

    assert symsystem1.output_eqns == out_eqns

    assert symsystem1.bodies == (Pa,)
    assert symsystem1.loads == ((P, g * m * N.x),)

