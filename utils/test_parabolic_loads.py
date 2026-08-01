
def test_parabolic_loads():

    E, I, L = symbols('E, I, L', positive=True, real=True)
    R, M, P = symbols('R, M, P', real=True)

    # cantilever beam fixed at x=0 and parabolic distributed loading across
    # length of beam
    beam = Beam(L, E, I)

    beam.bc_deflection.append((0, 0))
    beam.bc_slope.append((0, 0))
    beam.apply_load(R, 0, -1)
    beam.apply_load(M, 0, -2)

    # parabolic load
    beam.apply_load(1, 0, 2)

    beam.solve_for_reaction_loads(R, M)

    assert beam.reaction_loads[R] == -L**3/3

    # cantilever beam fixed at x=0 and parabolic distributed loading across
    # first half of beam
    beam = Beam(2*L, E, I)

    beam.bc_deflection.append((0, 0))
    beam.bc_slope.append((0, 0))
    beam.apply_load(R, 0, -1)
    beam.apply_load(M, 0, -2)

    # parabolic load from x=0 to x=L
    beam.apply_load(1, 0, 2, end=L)

    beam.solve_for_reaction_loads(R, M)

    # result should be the same as the prior example
    assert beam.reaction_loads[R] == -L**3/3

    # check constant load
    beam = Beam(2*L, E, I)
    beam.apply_load(P, 0, 0, end=L)
    loading = beam.load.xreplace({L: 10, E: 20, I: 30, P: 40})
    assert loading.xreplace({x: 5}) == 40
    assert loading.xreplace({x: 15}) == 0

    # check ramp load
    beam = Beam(2*L, E, I)
    beam.apply_load(P, 0, 1, end=L)
    assert beam.load == (P*SingularityFunction(x, 0, 1) -
                         P*SingularityFunction(x, L, 1) -
                         P*L*SingularityFunction(x, L, 0))

    # check higher order load: x**8 load from x=0 to x=L
    beam = Beam(2*L, E, I)
    beam.apply_load(P, 0, 8, end=L)
    loading = beam.load.xreplace({L: 10, E: 20, I: 30, P: 40})
    assert loading.xreplace({x: 5}) == 40*5**8
    assert loading.xreplace({x: 15}) == 0

