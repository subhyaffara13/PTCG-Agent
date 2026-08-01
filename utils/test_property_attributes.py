
def test_property_attributes():
    symsystem = SymbolicSystem(states, comb_explicit_rhs,
                               alg_con=alg_con_full, output_eqns=out_eqns,
                               coord_idxs=coord_idxs, speed_idxs=speed_idxs,
                               bodies=bodies, loads=loads)

    with raises(AttributeError):
        symsystem.bodies = 42
    with raises(AttributeError):
        symsystem.coordinates = 42
    with raises(AttributeError):
        symsystem.dyn_implicit_rhs = 42
    with raises(AttributeError):
        symsystem.comb_implicit_rhs = 42
    with raises(AttributeError):
        symsystem.loads = 42
    with raises(AttributeError):
        symsystem.dyn_implicit_mat = 42
    with raises(AttributeError):
        symsystem.comb_implicit_mat = 42
    with raises(AttributeError):
        symsystem.kin_explicit_rhs = 42
    with raises(AttributeError):
        symsystem.comb_explicit_rhs = 42
    with raises(AttributeError):
        symsystem.speeds = 42
    with raises(AttributeError):
        symsystem.states = 42
    with raises(AttributeError):
        symsystem.alg_con = 42

